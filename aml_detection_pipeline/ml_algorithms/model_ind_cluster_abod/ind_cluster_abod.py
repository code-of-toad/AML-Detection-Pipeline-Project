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
# For now (March 31st 2:22am), as long as within_clustering.py and within_ind_cluster.py
# is run before this one, we can just pull ind1_vAF.to_csv("cluster_csvs/ind1.csv")
ind1_vAF = pd.read_csv("cluster_csvs/ind1.csv", index_col="customer_id")
ind2_vAF = pd.read_csv("cluster_csvs/ind2.csv", index_col="customer_id")
ind3_vAF = pd.read_csv("cluster_csvs/ind3.csv", index_col="customer_id")
ind4_vAF = pd.read_csv("cluster_csvs/ind4.csv", index_col="customer_id")
ind5_vAF = pd.read_csv("cluster_csvs/ind5.csv", index_col="customer_id")
ind6_vAF = pd.read_csv("cluster_csvs/ind6.csv", index_col="customer_id")




# %%
# ---------------------------------------------------------------------------
# CLUSTER 1 FastABOD Rank-Stability
# n = 1844
# ---------------------------------------------------------------------------
ks = list(range(40, 180, 10))

n = 1844
ids_to_track = [
    "SYNID0104376482",
    "SYNID0104182767",
    "SYNID0103438850",
    "SYNID0102483979",
    "SYNID0109985345",
    "SYNID0107002167",
    "SYNID0104110691",
    "SYNID0108483390",
    "SYNID0108769446",
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(ind1_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=ind1_vAF.index,
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
    os.path.join("within_cluster_outputs", "tracked_rank_movement_ind1_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD (ind1): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 1 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 100
n_boot = 20
n_sub = int(len(ind1_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(ind1_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(ind1_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"ind1_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 1 FINAL MODEL
k_final = 100

ind1_abod_scores = pd.Series(
    scores_dict[k_final],
    index=ind1_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-ind1_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

ind1_abod_kfinal = (
    pd.DataFrame({
        "customer_id": ind1_abod_scores.index,
        "abod_score": abod_scaled,
        "abod_score_raw": ind1_abod_scores.values,
    })
    .sort_values(["abod_score", "abod_score_raw"], ascending=[False, False])
)

ind1_abod_kfinal = ind1_abod_kfinal[["customer_id", "abod_score"]]

ind1_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"ind1_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (IND1 n = 1844, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (IND1 n = 1844, k={k_final})")
plt.grid(True)
plt.show()




# %%
# ---------------------------------------------------------------------------
# CLUSTER 2 FastABOD Rank-Stability
# n = 15886
# ---------------------------------------------------------------------------
ks = list(range(40, 180, 20))

n = 15886
ids_to_track = [
    "SYNID0106250697",
    "SYNID0102062788",
    "SYNID0102207375",
    "SYNID0109902085",
    "SYNID0107464935", #LABELED
    "SYNID0107917985",
    "SYNID0101175231",
    "SYNID0107832828", #LABELED
    "SYNID0106740944",
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(ind2_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=ind2_vAF.index,
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
    os.path.join("within_cluster_outputs", "tracked_rank_movement_ind2_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD (ind2): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 2 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 100
n_boot = 100
n_sub = int(len(ind2_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(ind2_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(ind2_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"ind2_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 2 FINAL MODEL
k_final = 100

ind2_abod_model = ABOD(contamination=0.01, method="fast", n_neighbors=k_final)
ind2_abod_model.fit(ind2_vAF)

ind2_abod_scores = pd.Series(
    ind2_abod_model.decision_scores_,
    index=ind2_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-ind2_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

ind2_abod_kfinal = (
    pd.DataFrame({
        "customer_id": ind2_abod_scores.index,
        "abod_score": abod_scaled,
        "abod_score_raw": ind2_abod_scores.values,
    })
    .sort_values(["abod_score", "abod_score_raw"], ascending=[False, False])
)

ind2_abod_kfinal = ind2_abod_kfinal[["customer_id", "abod_score"]]

ind2_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"ind2_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (IND2 n = 15886, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (IND2 n = 15886, k={k_final})")
plt.grid(True)
plt.show()




# %%
# ---------------------------------------------------------------------------
# CLUSTER 3 FastABOD Rank-Stability
# n = 15659
# ---------------------------------------------------------------------------
ks = list(range(40, 180, 20))

n = 15659
ids_to_track = [
    "SYNID0109721547",
    "SYNID0105828615",
    "SYNID0106616060",
    "SYNID0106498007",
    "SYNID0100678396",
    "SYNID0100957188", # LABELED
    "SYNID0100498206",
    "SYNID0105755297",
    "SYNID0102776824",
    "SYNID0102007433",
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(ind3_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=ind3_vAF.index,
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
    os.path.join("within_cluster_outputs", "tracked_rank_movement_ind3_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD (ind3): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 3 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 100
n_boot = 100
n_sub = int(len(ind3_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(ind3_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(ind3_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"ind3_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 3 FINAL MODEL
k_final = 100

ind3_abod_model = ABOD(contamination=0.01, method="fast", n_neighbors=k_final)
ind3_abod_model.fit(ind3_vAF)

ind3_abod_scores = pd.Series(
    ind3_abod_model.decision_scores_,
    index=ind3_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-ind3_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

ind3_abod_kfinal = (
    pd.DataFrame({
        "customer_id": ind3_abod_scores.index,
        "abod_score": abod_scaled,
        "abod_score_raw": ind3_abod_scores.values,
    })
    .sort_values(["abod_score", "abod_score_raw"], ascending=[False, False])
)

ind3_abod_kfinal = ind3_abod_kfinal[["customer_id", "abod_score"]]

ind3_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"ind3_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (IND3 n = 15659, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (IND3 n = 15659, k={k_final})")
plt.grid(True)
plt.show()




# %%
# ---------------------------------------------------------------------------
# CLUSTER 4 FastABOD Rank-Stability
# n = 3892
# ---------------------------------------------------------------------------
ks = list(range(30, 60, 10))

n = 3892
ids_to_track = [
    "SYNID0108229005",
    "SYNID0103491795",
    "SYNID0101007903",
    "SYNID0100876697",
    "SYNID0108239278",
    "SYNID0109420236",
    "SYNID0104094489",
    "SYNID0104700085",
    "SYNID0108869499",
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(ind4_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=ind4_vAF.index,
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
    os.path.join("within_cluster_outputs", "tracked_rank_movement_ind4_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD IND4: rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 4 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 60
n_boot = 100
n_sub = int(len(ind4_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(ind4_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(ind4_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"ind4_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 4 FINAL MODEL
k_final = 60

ind4_abod_model = ABOD(contamination=0.01, method="fast", n_neighbors=k_final)
ind4_abod_model.fit(ind4_vAF)

ind4_abod_scores = pd.Series(
    ind4_abod_model.decision_scores_,
    index=ind4_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-ind4_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

ind4_abod_kfinal = (
    pd.DataFrame({
        "customer_id": ind4_abod_scores.index,
        "abod_score": abod_scaled,
        "abod_score_raw": ind4_abod_scores.values,
    })
    .sort_values(["abod_score", "abod_score_raw"], ascending=[False, False])
)

ind4_abod_kfinal = ind4_abod_kfinal[["customer_id", "abod_score"]]

ind4_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"ind4_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (IND4 n = 3892, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (IND4 n = 3892, k={k_final})")
plt.grid(True)
plt.show()




# %%
# ---------------------------------------------------------------------------
# CLUSTER 5 FastABOD Rank-Stability
# n = 14509
# ---------------------------------------------------------------------------
ks = list(range(40, 180, 20))

n = 14509
ids_to_track = [
    "SYNID0105740687",
    "SYNID0101819452",
    "SYNID0106912407",
    "SYNID0108180520",
    "SYNID0105593361", # LABELED
    "SYNID0101931021",
    "SYNID0105390238",
    "SYNID0107334515", # LABELED
    "SYNID0103953541",
    "SYNID0102714559",
    "SYNID0109764426",
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(ind5_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=ind5_vAF.index,
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
    os.path.join("within_cluster_outputs", "tracked_rank_movement_ind5_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD (ind5): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 5 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 50
n_boot = 100
n_sub = int(len(ind5_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(ind5_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(ind5_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"ind5_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 5 FINAL MODEL
k_final = 50

ind5_abod_model = ABOD(contamination=0.01, method="fast", n_neighbors=k_final)
ind5_abod_model.fit(ind5_vAF)

ind5_abod_scores = pd.Series(
    ind5_abod_model.decision_scores_,
    index=ind5_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-ind5_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

ind5_abod_kfinal = (
    pd.DataFrame({
        "customer_id": ind5_abod_scores.index,
        "abod_score": abod_scaled,
        "abod_score_raw": ind5_abod_scores.values,
    })
    .sort_values(["abod_score", "abod_score_raw"], ascending=[False, False])
)

ind5_abod_kfinal = ind5_abod_kfinal[["customer_id", "abod_score"]]

ind5_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"ind5_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (IND5 n = 14509, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (IND5 n = 14509, k={k_final})")
plt.grid(True)
plt.show()




# %%
# ---------------------------------------------------------------------------
# CLUSTER 6 FastABOD Rank-Stability
# n = 1309
# ---------------------------------------------------------------------------
ks = list(range(10, 60, 10))

n = 1309
ids_to_track = [
    "SYNID0107620196",
    "SYNID0101567239",
    "SYNID0107939725",
    "SYNID0102067497",
    "SYNID0106937634",
    "SYNID0105018060",
    "SYNID0105274297",
    "SYNID0105543086",
    "SYNID0109957203",
    "SYNID0101011377",
    "SYNID0107381497",
    "SYNID0102664065",
    "SYNID0105727635",
    "SYNID0101565132",
    "SYNID0109787005",
]

rank_by_k_cln = {}
scores_dict = {}

for k in ks:
    abod = ABOD(contamination=0.01,
               method="fast",
               n_neighbors=k)
    _ = abod.fit(ind6_vAF)

    abod_scores = pd.Series(
        abod.decision_scores_,
        index=ind6_vAF.index,
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
    os.path.join("within_cluster_outputs", "tracked_rank_movement_ind6_ABOD.csv"),
    index=False
)

plt.figure()
for cid, g in tracked_cln.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.title("ABOD IND6: rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# ---------------------------------------------------------------------------
# CLUSTER 6 BAGGING VALIDATION
# ---------------------------------------------------------------------------
k_bag = 20 
n_boot = 100
n_sub = int(len(ind6_vAF) * 0.8)  # 80% subsample without replacement
boot_ranks = []

for i in range(n_boot):
    X_sub = resample(ind6_vAF, replace=False, n_samples=n_sub, random_state=i)
    abod = ABOD(method="fast", n_neighbors=k_bag, contamination=0.01)
    abod.fit(X_sub)
    ranks = pd.Series(
        abod.decision_scores_, index=X_sub.index
    ).rank(method="min", ascending=False)
    boot_ranks.append(ranks)

# Align all runs to the full index before aggregating
boot_df = pd.concat(boot_ranks, axis=1).reindex(ind6_vAF.index)

# For each point, compute median rank and IQR across bootstraps
# (NaNs occur for iterations where a point wasn't sampled — excluded from stats)
summary = pd.DataFrame({
    "median_rank": boot_df.median(axis=1),
    "iqr": boot_df.quantile(0.75, axis=1) - boot_df.quantile(0.25, axis=1),
    "pct_top50": (boot_df <= 50).mean(axis=1)
}, index=boot_df.index).sort_values("median_rank")

summary.to_csv(os.path.join("within_cluster_outputs", f"ind6_abod_bagging_k{k_bag}.csv"))
# %%
# ---------------------------------------------------------------------------
# CLUSTER 6 FINAL MODEL
k_final = 20

ind6_abod_model = ABOD(contamination=0.01, method="fast", n_neighbors=k_final)
ind6_abod_model.fit(ind6_vAF)

ind6_abod_scores = pd.Series(
    ind6_abod_model.decision_scores_,
    index=ind6_vAF.index,
    name="abod_score"
)
# %%
log_scores = -np.log(-ind6_abod_scores)

abod_scaled = normalize_to_unit_interval(log_scores,
                                         flip_sign=False)

ind6_abod_kfinal = (
    pd.DataFrame({
        "customer_id": ind6_abod_scores.index,
        "abod_score": abod_scaled,
        "abod_score_raw": ind6_abod_scores.values,
    })
    .sort_values(["abod_score", "abod_score_raw"], ascending=[False, False])
)

ind6_abod_kfinal = ind6_abod_kfinal[["customer_id", "abod_score"]]

ind6_abod_kfinal.to_csv(
    os.path.join("within_cluster_outputs", f"ind6_abod_k{k_final}.csv"),
    index=False,
    float_format="%.6f"
)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(log_scores, bins=int(np.sqrt(len(log_scores))), edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title(f"Distribution of ABOD Scores, log scale (IND6 n = 1309, k={k_final})")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(abod_scaled, bins=int(np.sqrt(len(abod_scaled))), edgecolor="black")
plt.xlabel("Normalized ABOD Score (log-transformed)")
plt.ylabel("Count")
plt.title(f"Distribution of Normalized ABOD Scores (IND6 n = 1309, k={k_final})")
plt.grid(True)
plt.show()




# %%
# --------------------------------------------------------------
# SCORES ONLY FOR RULE BASED ALGO
# --------------------------------------------------------------

# Combine all raw ABOD scores across clusters into one Series
all_abod_scores = pd.concat([
    ind1_abod_scores,
    ind2_abod_scores,
    ind3_abod_scores,
    ind4_abod_scores,
    ind5_abod_scores,
    ind6_abod_scores,
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

ind1_global = compute_global_abod_extremeness(ind1_abod_scores)
ind2_global = compute_global_abod_extremeness(ind2_abod_scores)
ind3_global = compute_global_abod_extremeness(ind3_abod_scores)
ind4_global = compute_global_abod_extremeness(ind4_abod_scores)
ind5_global = compute_global_abod_extremeness(ind5_abod_scores)
ind6_global = compute_global_abod_extremeness(ind6_abod_scores)

# %%
indVA_ABOD_SCORES = pd.concat([
    ind1_global,
    ind2_global,
    ind3_global,
    ind4_global,
    ind5_global,
    ind6_global,
], axis=0, ignore_index=True)

indVA_ABOD_SCORES.to_csv("indVA_ABOD_SCORES.csv", index=False)

# %%
# PLOT OF RAW SCORES (log-transformed)
plt.figure()
plt.hist(all_log_scores, bins=100, edgecolor="black")
plt.xlabel("−log(−ABOD Score)")
plt.ylabel("Count")
plt.title("Distribution of Raw ABOD Scores, log scale (All IND Clusters)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(indVA_ABOD_SCORES["within_cluster_extremeness"], bins=100, edgecolor="black")
plt.xlabel("Within-Cluster Extremeness")
plt.ylabel("Count")
plt.title("Distribution of Normalized ABOD Scores (All IND Clusters)")
plt.grid(True)
plt.show()
# %%
