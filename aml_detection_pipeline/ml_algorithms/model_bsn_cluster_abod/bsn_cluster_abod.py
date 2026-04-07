# %%
# --------------------------------------------------------------
# Dependecies
# --------------------------------------------------------------
from pyod.models.abod import ABOD

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample
import os
os.makedirs("cluster_csvs", exist_ok=True)

from data_preprocessing import normalize_to_unit_interval

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

# %%
# --------------------------------------------------------------
# Pulling Data
# --------------------------------------------------------------
# For now (March 31st 2:22am), as long as within_clustering.py and within_bsn_cluster.py 
# is run before this one, we can just pull ind1_vAF.to_csv("cluster_csvs/ind1.csv")
bsn1_vAF = pd.read_csv("cluster_csvs/bsn1.csv", index_col="customer_id")
bsn2_vAF = pd.read_csv("cluster_csvs/bsn2.csv", index_col="customer_id")
bsn3_vAF = pd.read_csv("cluster_csvs/bsn3.csv", index_col="customer_id")
bsn4_vAF = pd.read_csv("cluster_csvs/bsn4.csv", index_col="customer_id")
bsn5_vAF = pd.read_csv("cluster_csvs/bsn5.csv", index_col="customer_id")
bsn6_vAF = pd.read_csv("cluster_csvs/bsn6.csv", index_col="customer_id")






# %%
# ---------------------------------------------------------------------------
# CLUSTER 1 FastABOD Rank-Stability 
# n = 4004
# ---------------------------------------------------------------------------
ks = list(range(20, 120, 10)) # Large n so anchor around square root n

n = 4004
ids_to_track = [ # Tracking the same ones from LOF models
    "SYNID0200537412",
    "SYNID0200740142",
    "SYNID0200579553",
    "SYNID0200209668",
    "SYNID0200755995", #LABELED
    "SYNID0200262977",
    "SYNID0200736127",
    "SYNID0200496670", #LABELED
    "SYNID0200863032",
    "SYNID0200742718",
    "SYNID0200540751",
    "SYNID0200591686",
]

rank_by_k_cln = {}
scores_dict = {}

# Since rank-stability is being used to pick k and we are using
# raw scores anyways, no need for 

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(bsn1_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=bsn1_vAF.index,
        name="abod_score"
    )

    scores_dict[k] = abod.decision_scores_


    # ranks for movement plot (1 = most outlier)
    rank_by_k_cln[k] = abod_scores.rank(method="min", ascending=False).astype(int)

# %%
# MOVEMENT TABLE AND PLOT
ranks_df_cln = pd.DataFrame(rank_by_k_cln)

tracked_cln = (
    ranks_df_cln.loc[ranks_df_cln.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked_cln["k"] = tracked_cln["k"].astype(int)
tracked_cln = tracked_cln.sort_values(["customer_id", "k"])
tracked_cln.to_csv(
    os.path.join("within_cluster_outputs", "tracked_rank_movement_bsn1_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD (bsn1): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 1 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 60
n_boot = 100
n_sub = int(len(bsn1_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(bsn1_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(bsn1_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", "bsn1_abod_bagging_k60.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 1 FINAL MODEL
k_final = 60

bsn1_abod_scores = pd.Series(
    scores_dict[k_final],
    index=bsn1_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-bsn1_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

bsn1_abod_kfinal = (
    pd.DataFrame({
        "customer_id": bsn1_abod_scores.index,
        "abod_score": abod_scaled,
        "median_rank": summary["median_rank"],
    })
    .sort_values(["abod_score", "median_rank"], ascending=[False, True])
)

bsn1_abod_kfinal = bsn1_abod_kfinal[["customer_id", "abod_score"]]

bsn1_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"bsn1_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (BSN1 n = 4004, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (BSN1 n = 4004, k={k_final})")
plt.grid(True)
plt.show()






# %%
# ---------------------------------------------------------------------------
# CLUSTER 2 FULL ABOD
# n = 618
# ---------------------------------------------------------------------------

# CLUSTER 2 FINAL MODEL
bsn2_abod_model = ABOD(contamination=0.01,
                        method="default")

_ = bsn2_abod_model.fit(bsn2_vAF)

bsn2_abod_scores = pd.Series(
        bsn2_abod_model.decision_scores_,
        index=bsn2_vAF.index,
        name="abod_score"
    )
# %%
log_scores = -np.log(-bsn2_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

bsn2_abod_full = (
    pd.DataFrame({
        "customer_id": bsn2_abod_scores.index,
        "abod_score": abod_scaled
    })
    .sort_values(["abod_score"], ascending=[False])
)

bsn2_abod_full = bsn2_abod_full[["customer_id", "abod_score"]]

bsn2_abod_full.to_csv(
    os.path.join("within_cluster_outputs", "bsn2_abod_full.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title("Distribution of ABOD Scores, log scale (BSN2 n = 618)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title("Distribution of Normalized ABOD Scores (BSN2 n = 618)")
plt.grid(True)
plt.show()






# %%
# ---------------------------------------------------------------------------
# CLUSTER 3 FULL ABOD
# n = 196
# ---------------------------------------------------------------------------

# CLUSTER 3 FINAL MODEL
bsn3_abod_model = ABOD(contamination=0.01,
                        method="default")

_ = bsn3_abod_model.fit(bsn3_vAF)

bsn3_abod_scores = pd.Series(
        bsn3_abod_model.decision_scores_,
        index=bsn3_vAF.index,
        name="abod_score"
    )
# %%
log_scores = -np.log(-bsn3_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

bsn3_abod_full = (
    pd.DataFrame({
        "customer_id": bsn3_abod_scores.index,
        "abod_score": abod_scaled
    })
    .sort_values(["abod_score"], ascending=[False])
)

bsn3_abod_full = bsn3_abod_full[["customer_id", "abod_score"]]

bsn3_abod_full.to_csv(
    os.path.join("within_cluster_outputs", "bsn3_abod_full.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title("Distribution of ABOD Scores, log scale (BSN3 n = 196)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title("Distribution of Normalized ABOD Scores (BSN3 n = 196)")
plt.grid(True)
plt.show()





# %%
# ---------------------------------------------------------------------------
# CLUSTER 4 FastABOD Rank-Stability 
# n = 2687
# ---------------------------------------------------------------------------
ks = list(range(40, 100, 20)) # Large n so anchor around square root n

n = 2687
ids_to_track = [ # Tracking the same ones from LOF models
    "SYNID0200342378",
    "SYNID0200577263",
    "SYNID0200937170",
    "SYNID0200982607",
    "SYNID0200755574", # LABELED
    "SYNID0200350995",
    "SYNID0200945958",
    "SYNID0200964318",
    "SYNID0200660991"
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(bsn4_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=bsn4_vAF.index,
        name="abod_score"
    )

    scores_dict[k] = abod.decision_scores_


    # ranks for movement plot (1 = most outlier)
    rank_by_k_cln[k] = abod_scores.rank(method="min", ascending=False).astype(int)

# %%
# MOVEMENT TABLE AND PLOT ---------------------------------------------------------------
ranks_df_cln = pd.DataFrame(rank_by_k_cln)

tracked_cln = (
    ranks_df_cln.loc[ranks_df_cln.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked_cln["k"] = tracked_cln["k"].astype(int)
tracked_cln = tracked_cln.sort_values(["customer_id", "k"])
tracked_cln.to_csv(
    os.path.join("within_cluster_outputs", "tracked_rank_movement_bsn4_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD BSN4: rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 4 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 80 # we w
n_boot = 100
n_sub = int(len(bsn4_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(bsn4_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(bsn4_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"bsn4_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 4 FINAL MODEL
k_final = 80

bsn4_abod_scores = pd.Series(
    scores_dict[k_final],
    index=bsn4_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-bsn4_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

bsn4_abod_kfinal = (
    pd.DataFrame({
        "customer_id": bsn4_abod_scores.index,
        "abod_score": abod_scaled,
        "median_rank": summary["median_rank"],
    })
    .sort_values(["abod_score", "median_rank"], ascending=[False, True])
)

bsn4_abod_kfinal = bsn4_abod_kfinal[["customer_id", "abod_score"]]

bsn4_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"bsn4_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (BSN4 n = 2687, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (BSN4 n = 2687, k={k_final})")
plt.grid(True)
plt.show()





# %%
# ---------------------------------------------------------------------------
# CLUSTER 5 FULL ABOD
# n = 108
# ---------------------------------------------------------------------------

# CLUSTER 5 FINAL MODEL
bsn5_abod_model = ABOD(contamination=0.01,
                        method="default")

_ = bsn5_abod_model.fit(bsn5_vAF)

bsn5_abod_scores = pd.Series(
        bsn5_abod_model.decision_scores_,
        index=bsn5_vAF.index,
        name="abod_score"
    )
# %%
log_scores = -np.log(-bsn5_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

bsn5_abod_full = (
    pd.DataFrame({
        "customer_id": bsn5_abod_scores.index,
        "abod_score": abod_scaled
    })
    .sort_values(["abod_score"], ascending=[False])
)

bsn5_abod_full = bsn5_abod_full[["customer_id", "abod_score"]]

bsn5_abod_full.to_csv(
    os.path.join("within_cluster_outputs", "bsn5_abod_full.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title("Distribution of ABOD Scores, log scale (BSN5 n = 108)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title("Distribution of Normalized ABOD Scores (BSN5 n = 108)")
plt.grid(True)
plt.show()





# %%
# ---------------------------------------------------------------------------
# CLUSTER 6 FULL ABOD
# n = 698
# ---------------------------------------------------------------------------
ks = list(range(30, 100, 20)) # Large n so anchor around square root n

n = 698
ids_to_track = ["SYNID0200390751", # TOP 6
                "SYNID0200812065",
                "SYNID0200965745",
                "SYNID0200834817",
                "SYNID0200061993",
                "SYNID0200778085", 
                "SYNID0200906624", # BOTTOM 3
                "SYNID0200105323",
                "SYNID0200224000",
                "SYNID0200878172", # MIDDLE 3
                "SYNID0200133385",
                "SYNID0200320704"
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(bsn6_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=bsn6_vAF.index,
        name="abod_score"
    )

    scores_dict[k] = abod.decision_scores_


    # ranks for movement plot (1 = most outlier)
    rank_by_k_cln[k] = abod_scores.rank(method="min", ascending=False).astype(int)

# %%
# MOVEMENT TABLE AND PLOT ---------------------------------------------------------------
ranks_df_cln = pd.DataFrame(rank_by_k_cln)

tracked_cln = (
    ranks_df_cln.loc[ranks_df_cln.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked_cln["k"] = tracked_cln["k"].astype(int)
tracked_cln = tracked_cln.sort_values(["customer_id", "k"])
tracked_cln.to_csv(
    os.path.join("within_cluster_outputs", "tracked_rank_movement_bsn6_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD BSN6: rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 6 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 70
n_boot = 100
n_sub = int(len(bsn6_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(bsn6_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(bsn6_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"bsn6_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 6 FINAL MODEL
k_final = 70

bsn6_abod_scores = pd.Series(
    scores_dict[k_final],
    index=bsn6_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-bsn6_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

bsn6_abod_kfinal = (
    pd.DataFrame({
        "customer_id": bsn6_abod_scores.index,
        "abod_score": abod_scaled,
        "median_rank": summary["median_rank"],
    })
    .sort_values(["abod_score", "median_rank"], ascending=[False, True])
)

bsn6_abod_kfinal = bsn6_abod_kfinal[["customer_id", "abod_score"]]

bsn6_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"bsn6_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (BSN6 n = 698, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (BSN6 n = 698, k={k_final})")
plt.grid(True)
plt.show()






# %%
# --------------------------------------------------------------
# SCORES ONLY FOR RULE BASED ALGO
# --------------------------------------------------------------

# Combine all raw ABOD scores across clusters into one Series
all_abod_scores = pd.concat([
    bsn1_abod_scores,
    bsn2_abod_scores,
    bsn3_abod_scores,
    bsn4_abod_scores,
    bsn5_abod_scores,
    bsn6_abod_scores,
])

# Log transform so higher = more anomalous
all_log_scores = -np.log(-all_abod_scores)

# Robust scaling using 1st and 99th percentile to avoid extreme outlier compression
p1 = all_log_scores.quantile(0.01)
p99 = all_log_scores.quantile(0.99)

def compute_global_abod_extremeness(abod_scores):
    log_s = -np.log(-abod_scores)
    scaled = ((log_s - p1) / (p99 - p1)).clip(0, 1)
    return pd.DataFrame({
        "customer_id": abod_scores.index,
        "within_cluster_extremeness": scaled
    })

bsn1_global = compute_global_abod_extremeness(bsn1_abod_scores)
bsn2_global = compute_global_abod_extremeness(bsn2_abod_scores)
bsn3_global = compute_global_abod_extremeness(bsn3_abod_scores)
bsn4_global = compute_global_abod_extremeness(bsn4_abod_scores)
bsn5_global = compute_global_abod_extremeness(bsn5_abod_scores)
bsn6_global = compute_global_abod_extremeness(bsn6_abod_scores)

# %%
bsnVA_ABOD_SCORES = pd.concat([
    bsn1_global,
    bsn2_global,
    bsn3_global,
    bsn4_global,
    bsn5_global,
    bsn6_global,
], axis=0, ignore_index=True)

bsnVA_ABOD_SCORES.to_csv("bsnVA_ABOD_SCORES.csv", index=False)

# %%
# PLOT OF RAW SCORES (log-transformed)
plt.figure()
plt.hist(all_log_scores, bins=100, edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title("Distribution of Raw ABOD Scores, log scale (All BSN Clusters)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(bsnVA_ABOD_SCORES["within_cluster_extremeness"], bins=100, edgecolor="black")
plt.xlabel("Within-Cluster Extremeness")
plt.ylabel("Count")
plt.title("Distribution of Normalized ABOD Scores (All BSN Clusters)")
plt.grid(True)
plt.show()

# %%
# Combine with individual ABOD scores
indVA_ABOD_SCORES = pd.read_csv("indVA_ABOD_SCORES.csv")

clustered_ABOD_scores = pd.concat([indVA_ABOD_SCORES, bsnVA_ABOD_SCORES], axis=0, ignore_index=True)

clustered_ABOD_scores.to_csv("clustered_ABOD_scores.csv", index=False)
clustered_ABOD_scores.head()
# %%
# PLOT OF NORMALIZED SCORES (All IND + BSN Clusters)
plt.figure()
plt.hist(clustered_ABOD_scores["within_cluster_extremeness"], bins=100, edgecolor="black")
plt.xlabel("Within-Cluster Extremeness")
plt.ylabel("Count")
plt.title("Distribution of Normalized ABOD Scores (All Clusters)")
plt.grid(True)
plt.show()

# %%
