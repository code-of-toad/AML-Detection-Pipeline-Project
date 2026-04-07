# %%
# --------------------------------------------------------------
# Dependecies
# --------------------------------------------------------------
from sklearn.neighbors import LocalOutlierFactor

import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("cluster_csvs", exist_ok=True)
import numpy as np

from data_preprocessing import normalize_to_unit_interval

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
# %%
# --------------------------------------------------------------
# Pulling Data
# --------------------------------------------------------------
businesses_vA = pd.read_csv(
    "/Users/dangernoodle_/Desktop/DATA/DataTables/businesses_vA_2.csv")
bsn_VA_FAMD = pd.read_csv(
    "/Users/dangernoodle_/Desktop/DATA/DataTables/VersionA_Business_AfterFAMD_2.csv")

# %%
# 1) Hard checks
if len(businesses_vA) != len(bsn_VA_FAMD):
    raise ValueError(f"Row count mismatch: customers={len(businesses_vA)} famd={len(bsn_VA_FAMD)}")

if "customer_id" not in businesses_vA.columns:
    raise ValueError("customers CSV must contain customer_id")

# 2) Attach by position safely
bsnVA_FAMD_output = bsn_VA_FAMD.copy()
bsnVA_FAMD_output.insert(0, "customer_id", businesses_vA["customer_id"].to_numpy())
bsnVA_FAMD_output.insert(1, "cluster", businesses_vA["cluster"].to_numpy())

# 3) Optional: assert uniqueness
if bsnVA_FAMD_output["customer_id"].duplicated().any():
    raise ValueError("customer_id is not unique in customers_business_only.csv (unexpected for a key).")

bsnVA_FAMD_output.to_csv("famd_with_customer_id.csv", index=False)

# %%
# --------------------------------------------------------------
# MAKING SUBSETS BY CLUSTER GROUPING
# --------------------------------------------------------------

# CLUSTER 6
bsn6_vAF = bsnVA_FAMD_output[bsnVA_FAMD_output["cluster"] == "business_6"]

# Dropping cluster type column
bsn6_vAF = bsn6_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
bsn6_vAF_copy = bsn6_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
bsn6_vAF = bsn6_vAF.set_index("customer_id", drop=True)
bsn6_vAF.to_csv("cluster_csvs/bsn6.csv")
#dfbsn6_vAF = bsn6_vAF.reset_index() to put back

# %%
# --------------------------------------------------------------
# LOCAL OUTLIER FACTOR first trial
# BSN6 needed fixed c = .05 resulting in k = 86
# --------------------------------------------------------------

# BSN6: n = 698 
bsn6_lof_model = LocalOutlierFactor(
    n_neighbors=115,
    contamination=.05,
    n_jobs=-1
    )

bsn6_lof_fitted = bsn6_lof_model.fit_predict(bsn6_vAF)

bsn6_lof_scores = pd.Series(
    bsn6_lof_model.negative_outlier_factor_,
    index=bsn6_vAF.index)

bsn6_scored = bsn6_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
bsn6_scored.loc[bsn6_lof_scores.index, "lof_score_raw"] = bsn6_lof_scores

lof_all_norm = normalize_to_unit_interval(bsn6_lof_scores)

df_out_bsn6 = (
    pd.DataFrame({
        "customer_id": bsn6_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": bsn6_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_bsn6 = df_out_bsn6[["customer_id", "outlier_score_01"]]

df_out_bsn6.to_csv("bsn6_LOF_k86_score.csv", index=False,
              float_format="%.10f")

top_ids = bsn6_lof_scores.sort_values(ascending=True).index
top_anomalies_bsn6 = bsn6_scored.loc[top_ids].copy()
top_anomalies_bsn6.to_csv("bsn6_LOF_k86.csv", index=False)

# %%
# --------------------------------------------------------------
# LOCAL OUTLIER FACTOR LOOP
# --------------------------------------------------------------
OUTPUT_DIR = "within_cluster_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ks = list(range(80, 200, 5))

TOP_N = 698

# BSN 6 did not capture any pre-labeled observations
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
                "SYNID0200320704"]

rank_by_k = {}

for k in ks:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination=.05,
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(bsn6_vAF)

    lof_scores = pd.Series(
        lof_loop.negative_outlier_factor_,
        index=bsn6_vAF.index,
        name="lof_score_raw"
    )

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the bsn6 table that has customer_id as a column
    bsn6_scored_k = bsn6_vAF_copy.copy()
    bsn6_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N).index
    top_anomalies_k = bsn6_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
        os.path.join(OUTPUT_DIR, f"bsn6_LOF_top{TOP_N}_k{k}.csv"),
        index=False
    )

# %%
# ----- movement table + plot
ranks_df = pd.DataFrame(rank_by_k)

tracked = (
    ranks_df.loc[ranks_df.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked["k"] = tracked["k"].astype(int)
tracked = tracked.sort_values(["customer_id", "k"])

tracked.to_csv(
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_bsn6_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(20, 0) #to change sclae of y-axis
plt.title("LOF (bsn6): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(bsn6_lof_scores, bins=int(np.sqrt(len(bsn6_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (BSN6)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(bsn6_lof_scores)

bsn6_lof_final = (
    pd.DataFrame({
        "customer_id": bsn6_lof_scores.index,
        "outlier_score_01": lof_scaled
    })
    .sort_values("outlier_score_01", ascending=False)
)

bsn6_lof_final = bsn6_lof_final[["customer_id", "outlier_score_01"]]

bsn6_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "bsn6_LOF_k115_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (BSN6 n = 698)")
plt.grid(True)
plt.show()




# %%
# --------------------------------------------------------------
# MAKING SUBSETS BY CLUSTER GROUPING
# --------------------------------------------------------------

# CLUSTER 5 --------------------------------------------------------------
bsn5_vAF = bsnVA_FAMD_output[bsnVA_FAMD_output["cluster"] == "business_5"]

# Dropping cluster type column
bsn5_vAF = bsn5_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
bsn5_vAF_copy = bsn5_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
bsn5_vAF = bsn5_vAF.set_index("customer_id", drop=True)
bsn5_vAF.to_csv("cluster_csvs/bsn5.csv")

# CLUSTER 4 --------------------------------------------------------------
bsn4_vAF = bsnVA_FAMD_output[bsnVA_FAMD_output["cluster"] == "business_4"]

# Dropping cluster type column
bsn4_vAF = bsn4_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
bsn4_vAF_copy = bsn4_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
bsn4_vAF = bsn4_vAF.set_index("customer_id", drop=True)
bsn4_vAF.to_csv("cluster_csvs/bsn4.csv")

# CLUSTER 3 -------------------------------------------------------------
bsn3_vAF = bsnVA_FAMD_output[bsnVA_FAMD_output["cluster"] == "business_3"]

# Dropping cluster type column
bsn3_vAF = bsn3_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
bsn3_vAF_copy = bsn3_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
bsn3_vAF = bsn3_vAF.set_index("customer_id", drop=True)
bsn3_vAF.to_csv("cluster_csvs/bsn3.csv")

# CLUSTER 2 -------------------------------------------------------------
bsn2_vAF = bsnVA_FAMD_output[bsnVA_FAMD_output["cluster"] == "business_2"]

# Dropping cluster type column
bsn2_vAF = bsn2_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
bsn2_vAF_copy = bsn2_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
bsn2_vAF = bsn2_vAF.set_index("customer_id", drop=True)
bsn2_vAF.to_csv("cluster_csvs/bsn2.csv")

# CLUSTER 1 -------------------------------------------------------------
bsn1_vAF = bsnVA_FAMD_output[bsnVA_FAMD_output["cluster"] == "business_1"]

# Dropping cluster type column
bsn1_vAF = bsn1_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
bsn1_vAF_copy = bsn1_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
bsn1_vAF = bsn1_vAF.set_index("customer_id", drop=True)
bsn1_vAF.to_csv("cluster_csvs/bsn1.csv")


# %%
# --------------------------------------------------------------
# CLUSTER 5 FIRST FIT
# --------------------------------------------------------------
# 108 rows
bsn5_lof_model = LocalOutlierFactor(
    n_neighbors=9,
    contamination=0.018571,
    n_jobs=-1
    )

bsn5_lof_fitted = bsn5_lof_model.fit_predict(bsn5_vAF)

bsn5_lof_scores = pd.Series(
    bsn5_lof_model.negative_outlier_factor_,
    index=bsn5_vAF.index)

bsn5_scored = bsn5_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
bsn5_scored.loc[bsn5_lof_scores.index, "lof_score_raw"] = bsn5_lof_scores

lof_all_norm = normalize_to_unit_interval(bsn5_lof_scores)

df_out_bsn5 = (
    pd.DataFrame({
        "customer_id": bsn5_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": bsn5_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_bsn5 = df_out_bsn5[["customer_id", "outlier_score_01"]]

df_out_bsn5.to_csv("bsn5_LOF_k9_score.csv", index=False,
              float_format="%.10f")

top_ids = bsn5_lof_scores.sort_values(ascending=True).index
top_anomalies_bsn5 = bsn5_scored.loc[top_ids].copy()
top_anomalies_bsn5.to_csv("bsn5_LOF_k9.csv", index=False)


pd.read_csv("bsn5_LOF_k9.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 5 LOOP
# --------------------------------------------------------------
k5 = list(range(8, 20, 1))

TOP_N_k5 = 108

ids_to_track = [
    "SYNID0200832632", #TOP 3
    "SYNID0200617860",
    "SYNID0200848282",
    "SYNID0200091933", #MIDDLE 3
    "SYNID0200315105",
    "SYNID0200331276",
    "SYNID0200303192", #BOTTOM 3
    "SYNID0200366245",
    "SYNID0200057679",]

rank_by_k = {}

for k in k5:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination='auto',
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(bsn5_vAF)

    lof_scores = pd.Series(
        lof_loop.negative_outlier_factor_,
        index=bsn5_vAF.index,
        name="lof_score_raw"
    )

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the bsn5 table that has customer_id as a column
    bsn5_scored_k = bsn5_vAF_copy.copy()
    bsn5_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k5).index
    top_anomalies_k = bsn5_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
        os.path.join(OUTPUT_DIR, f"bsn5_LOF_top{TOP_N_k5}_k{k}.csv"),
        index=False
    )

# ----- movement table + plot
ranks_df = pd.DataFrame(rank_by_k)

tracked = (
    ranks_df.loc[ranks_df.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked["k"] = tracked["k"].astype(int)
tracked = tracked.sort_values(["customer_id", "k"])

tracked.to_csv(
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_bsn5_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(25, 0) #to change sclae of y-axis
plt.title("LOF (bsn5): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(bsn5_lof_scores, bins=int(np.sqrt(len(bsn5_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (BSN5)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(bsn5_lof_scores)

bsn5_lof_final = (
    pd.DataFrame({
        "customer_id": bsn5_lof_scores.index,
        "outlier_score_01": lof_scaled
    })
    .sort_values("outlier_score_01", ascending=False)
)

bsn5_lof_final = bsn5_lof_final[["customer_id", "outlier_score_01"]]

bsn5_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "bsn5_LOF_k9_score.csv"),
    index=False,
    float_format="%.6f"
)

# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (BSN5 n = 108)")
plt.grid(True)
plt.show()


# %%
# --------------------------------------------------------------
# CLUSTER 4 FIRST FIT
# --------------------------------------------------------------
# 2687 rows
bsn4_lof_model = LocalOutlierFactor(
    n_neighbors=73,
    contamination=0.067041,
    n_jobs=-1
    )

bsn4_lof_fitted = bsn4_lof_model.fit_predict(bsn4_vAF)

bsn4_lof_scores = pd.Series(
    bsn4_lof_model.negative_outlier_factor_,
    index=bsn4_vAF.index)

bsn4_scored = bsn4_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
bsn4_scored.loc[bsn4_lof_scores.index, "lof_score_raw"] = bsn4_lof_scores

lof_all_norm = normalize_to_unit_interval(bsn4_lof_scores)

df_out_bsn4 = (
    pd.DataFrame({
        "customer_id": bsn4_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": bsn4_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_bsn4 = df_out_bsn4[["customer_id", "outlier_score_01"]]

df_out_bsn4.to_csv("bsn4_LOF_k73_score.csv", index=False,
              float_format="%.10f")

top_ids = bsn4_lof_scores.sort_values(ascending=True).index
top_anomalies_bsn4 = bsn4_scored.loc[top_ids].copy()
top_anomalies_bsn4.to_csv("bsn4_LOF_k73.csv", index=False)


pd.read_csv("bsn4_LOF_k73.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 4 LOOP
# --------------------------------------------------------------
k4 = list(range(50, 100, 5))

TOP_N_k4 = 2687

ids_to_track = [
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

rank_by_k = {}

for k in k4:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(bsn4_vAF)

    lof_scores = pd.Series(
        lof_loop.negative_outlier_factor_,
        index=bsn4_vAF.index,
        name="lof_score_raw"
    )

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the bsn4 table that has customer_id as a column
    bsn4_scored_k = bsn4_vAF_copy.copy()
    bsn4_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k4).index
    top_anomalies_k = bsn4_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
        os.path.join(OUTPUT_DIR, f"bsn4_LOF_top{TOP_N_k4}_k{k}.csv"),
        index=False
    )

# %%
# ----- movement table + plot
ranks_df = pd.DataFrame(rank_by_k)

tracked = (
    ranks_df.loc[ranks_df.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked["k"] = tracked["k"].astype(int)
tracked = tracked.sort_values(["customer_id", "k"])

tracked.to_csv(
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_bsn4_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(50, 0) #to change sclae of y-axis
plt.title("LOF (BSN4 n = 2687): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(bsn4_lof_scores, bins=int(np.sqrt(len(bsn4_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (BSN4)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(bsn4_lof_scores)

bsn4_lof_final = (
    pd.DataFrame({
        "customer_id": bsn4_lof_scores.index,
        "outlier_score_01": lof_scaled
    })
    .sort_values("outlier_score_01", ascending=False)
)

bsn4_lof_final = bsn4_lof_final[["customer_id", "outlier_score_01"]]

bsn4_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "bsn4_LOF_k73_score.csv"),
    index=False,
    float_format="%.6f"
)

# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (BSN4 n = 2687)")
plt.grid(True)
plt.show()


# %%
# --------------------------------------------------------------
# CLUSTER 3 FIRST FIT
# --------------------------------------------------------------
# 196 rows
bsn3_lof_model = LocalOutlierFactor(
    n_neighbors=6,
    contamination=0.057347,
    n_jobs=-1
    )

bsn3_lof_fitted = bsn3_lof_model.fit_predict(bsn3_vAF)

bsn3_lof_scores = pd.Series(
    bsn3_lof_model.negative_outlier_factor_,
    index=bsn3_vAF.index
)

bsn3_scored = bsn3_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
bsn3_scored.loc[bsn3_lof_scores.index, "lof_score_raw"] = bsn3_lof_scores

lof_all_norm = normalize_to_unit_interval(bsn3_lof_scores)

df_out_bsn3 = (
    pd.DataFrame({
        "customer_id": bsn3_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": bsn3_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_bsn3 = df_out_bsn3[["customer_id", "outlier_score_01"]]

df_out_bsn3.to_csv("bsn3_LOF_k6_score.csv", index=False,
              float_format="%.10f")

top_ids = bsn3_lof_scores.sort_values(ascending=True).index
top_anomalies_bsn3 = bsn3_scored.loc[top_ids].copy()
top_anomalies_bsn3.to_csv("bsn3_LOF_k6.csv", index=False)

pd.read_csv("bsn3_LOF_k6.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 3 LOOP
# --------------------------------------------------------------
k3 = list(range(5, 25, 5))

TOP_N_k3 = 196

ids_to_track = [
    "SYNID0200931678",
    "SYNID0200999280",
    "SYNID0200159270",
    "SYNID0200161910",
    "SYNID0200100125",
    "SYNID0200637929",
    "SYNID0200071595",
    "SYNID0200493584",
    "SYNID0200349306",
    "SYNID0200752981",
]

rank_by_k = {}

for k in k3:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(bsn3_vAF)

    lof_scores = pd.Series(
    lof_loop.negative_outlier_factor_,
    index=bsn3_vAF.index,
    name="lof_score_raw"
)

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the bsn3 table that has customer_id as a column
    bsn3_scored_k = bsn3_vAF_copy.copy()
    bsn3_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k3).index
    top_anomalies_k = bsn3_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
    os.path.join(OUTPUT_DIR, f"bsn3_LOF_top{TOP_N_k3}_k{k}.csv"),
    index=False
)

# %%
# ----- movement table + plot
ranks_df = pd.DataFrame(rank_by_k)

tracked = (
    ranks_df.loc[ranks_df.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked["k"] = tracked["k"].astype(int)
tracked = tracked.sort_values(["customer_id", "k"])

tracked.to_csv(
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_bsn3_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.ylim(20, 0)
plt.title("LOF (BSN3 n=196): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(bsn3_lof_scores, bins=int(np.sqrt(len(bsn3_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (BSN3)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(bsn3_lof_scores)

bsn3_lof_final = (
    pd.DataFrame({
        "customer_id": bsn3_lof_scores.index,
        "outlier_score_01": lof_scaled
    })
    .sort_values("outlier_score_01", ascending=False)
)

bsn3_lof_final = bsn3_lof_final[["customer_id", "outlier_score_01"]]

bsn3_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "bsn3_LOF_k6_score.csv"),
    index=False,
    float_format="%.6f"
)

# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (BSN3 n = 196)")
plt.grid(True)
plt.show()
# %%
# --------------------------------------------------------------
# CLUSTER 2 FIRST FIT
# --------------------------------------------------------------
# 618 rows
bsn2_lof_model = LocalOutlierFactor(
    n_neighbors=32,
    contamination=0.008878,
    n_jobs=-1
    )

bsn2_lof_fitted = bsn2_lof_model.fit_predict(bsn2_vAF)

bsn2_lof_scores = pd.Series(
    bsn2_lof_model.negative_outlier_factor_,
    index=bsn2_vAF.index
)

bsn2_scored = bsn2_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
bsn2_scored.loc[bsn2_lof_scores.index, "lof_score_raw"] = bsn2_lof_scores

lof_all_norm = normalize_to_unit_interval(bsn2_lof_scores)

df_out_bsn2 = (
    pd.DataFrame({
        "customer_id": bsn2_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": bsn2_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_bsn2 = df_out_bsn2[["customer_id", "outlier_score_01"]]

df_out_bsn2.to_csv("bsn2_LOF_k32_score.csv", index=False,
              float_format="%.10f")

top_ids = bsn2_lof_scores.sort_values(ascending=True).index
top_anomalies_bsn2 = bsn2_scored.loc[top_ids].copy()
top_anomalies_bsn2.to_csv("bsn2_LOF_top.csv", index=False)

pd.read_csv("bsn2_LOF_top.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 2 LOOP
# --------------------------------------------------------------
k2 = list(range(10, 50, 2))

TOP_N_k2 = 618

ids_to_track = [
    "SYNID0200057370",
    "SYNID0200414521",
    "SYNID0200983378",
    "SYNID0200700121",
    "SYNID0200187014",
    "SYNID0200006191",
    "SYNID0200565743",
    "SYNID0200693227",
    "SYNID0200784354",
]

rank_by_k = {}

for k in k2:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(bsn2_vAF)

    lof_scores = pd.Series(
    lof_loop.negative_outlier_factor_,
    index=bsn2_vAF.index,
    name="lof_score_raw"
)

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the bsn2 table that has customer_id as a column
    bsn2_scored_k = bsn2_vAF_copy.copy()
    bsn2_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k2).index
    top_anomalies_k = bsn2_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
    os.path.join(OUTPUT_DIR, f"bsn2_LOF_top{TOP_N_k2}_k{k}.csv"),
    index=False
)

# %%
# ----- movement table + plot
ranks_df = pd.DataFrame(rank_by_k)

tracked = (
    ranks_df.loc[ranks_df.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked["k"] = tracked["k"].astype(int)
tracked = tracked.sort_values(["customer_id", "k"])

tracked.to_csv(
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_bsn2_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(20, 0)
plt.title("LOF (bsn2): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(bsn2_lof_scores, bins=int(np.sqrt(len(bsn2_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (BSN2)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(bsn2_lof_scores)

bsn2_lof_final = (
    pd.DataFrame({
        "customer_id": bsn2_lof_scores.index,
        "outlier_score_01": lof_scaled
    })
    .sort_values("outlier_score_01", ascending=False)
)

bsn2_lof_final = bsn2_lof_final[["customer_id", "outlier_score_01"]]

bsn2_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "bsn2_LOF_k32_score.csv"),
    index=False,
    float_format="%.6f"
)

# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (BSN2 n = 618)")
plt.grid(True)
plt.show()


# %%
# --------------------------------------------------------------
# CLUSTER 1 FIRST FIT
# BSN1 needed fixed c = .01 resulting in k = 749
# --------------------------------------------------------------
# 4004 rows
bsn1_lof_model = LocalOutlierFactor(
    n_neighbors=749,
    contamination=.01,
    n_jobs=-1
    )

bsn1_lof_fitted = bsn1_lof_model.fit_predict(bsn1_vAF)

bsn1_lof_scores = pd.Series(
    bsn1_lof_model.negative_outlier_factor_,
    index=bsn1_vAF.index
)

bsn1_scored = bsn1_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
bsn1_scored.loc[bsn1_lof_scores.index, "lof_score_raw"] = bsn1_lof_scores

lof_all_norm = normalize_to_unit_interval(bsn1_lof_scores)

df_out_bsn1 = (
    pd.DataFrame({
        "customer_id": bsn1_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": bsn1_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_bsn1 = df_out_bsn1[["customer_id", "outlier_score_01"]]

df_out_bsn1.to_csv("bsn1_LOF_k749_scores.csv", index=False,
              float_format="%.10f")

top_ids = bsn1_lof_scores.sort_values(ascending=True).index
top_anomalies_bsn1 = bsn1_scored.loc[top_ids].copy()
top_anomalies_bsn1.to_csv("bsn1_LOF_top.csv", index=False)

pd.read_csv("bsn1_LOF_top.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 1 LOOP
# --------------------------------------------------------------
k1 = list(range(700, 900, 10))

TOP_N_k1 = 4004

ids_to_track = [
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

rank_by_k = {}

for k in k1:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(bsn1_vAF)

    lof_scores = pd.Series(
    lof_loop.negative_outlier_factor_,
    index=bsn1_vAF.index,
    name="lof_score_raw"
)

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the bsn1 table that has customer_id as a column
    bsn1_scored_k = bsn1_vAF_copy.copy()
    bsn1_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k1).index
    top_anomalies_k = bsn1_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
    os.path.join(OUTPUT_DIR, f"bsn1_LOF_top{TOP_N_k1}_k{k}.csv"),
    index=False
)

# %%
# ----- movement table + plot
ranks_df = pd.DataFrame(rank_by_k)

tracked = (
    ranks_df.loc[ranks_df.index.intersection(ids_to_track)]
    .reset_index(names="customer_id")
    .melt(id_vars="customer_id", var_name="k", value_name="rank")
)
tracked["k"] = tracked["k"].astype(int)
tracked = tracked.sort_values(["customer_id", "k"])

tracked.to_csv(
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_bsn1_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.ylim(50, 0)
plt.title("LOF (BSN1 n = 4004): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(bsn1_lof_scores, bins=int(np.sqrt(len(bsn1_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (BSN1)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(bsn1_lof_scores)

bsn1_lof_final = (
    pd.DataFrame({
        "customer_id": bsn1_lof_scores.index,
        "outlier_score_01": lof_scaled
    })
    .sort_values("outlier_score_01", ascending=False)
)

bsn1_lof_final = bsn1_lof_final[["customer_id", "outlier_score_01"]]

bsn1_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "bsn1_LOF_k749_score.csv"),
    index=False,
    float_format="%.6f"
)

# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (BSN1 n = 4004)")
plt.grid(True)
plt.show()




# %%
# --------------------------------------------------------------
# SCORES ONLY FOR RULE BASED ALGO
# --------------------------------------------------------------


# Combine all raw LOF scores across clusters into one Series
all_lof_scores = pd.concat([
    bsn1_lof_scores,
    bsn2_lof_scores,
    bsn3_lof_scores,
    bsn4_lof_scores,
    bsn5_lof_scores,
    bsn6_lof_scores,
])

# Negate so higher = more anomalous
global_severity = -all_lof_scores

# Robust scaling using 1st and 99th percentile to avoid extreme outlier compression
p1 = global_severity.quantile(0.01)
p99 = global_severity.quantile(0.99)

def compute_global_extremeness(scored_df, lof_scores):
    df_out = scored_df.copy()
    severity = -lof_scores.loc[df_out.index]
    df_out["within_cluster_extremeness"] = ((severity - p1) / (p99 - p1)).clip(0, 1)
    return df_out

top_anomalies_bsn1 = compute_global_extremeness(top_anomalies_bsn1, bsn1_lof_scores)
top_anomalies_bsn2 = compute_global_extremeness(top_anomalies_bsn2, bsn2_lof_scores)
top_anomalies_bsn3 = compute_global_extremeness(top_anomalies_bsn3, bsn3_lof_scores)
top_anomalies_bsn4 = compute_global_extremeness(top_anomalies_bsn4, bsn4_lof_scores)
top_anomalies_bsn5 = compute_global_extremeness(top_anomalies_bsn5, bsn5_lof_scores)
top_anomalies_bsn6 = compute_global_extremeness(top_anomalies_bsn6, bsn6_lof_scores)

# %%
bsnVA_SCORES = pd.concat([
    top_anomalies_bsn1[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_bsn2[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_bsn3[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_bsn4[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_bsn5[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_bsn6[["customer_id", "within_cluster_extremeness"]],
], axis=0, ignore_index=True)

bsnVA_SCORES.to_csv("bsnVA_SCORES.csv", index=False)

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(all_lof_scores, bins=100, edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of Raw LOF Scores (All Clusters)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(bsnVA_SCORES["within_cluster_extremeness"], bins=100, edgecolor="black")
plt.xlabel("Within-Cluster Extremeness")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (All BSN Clusters)")
plt.grid(True)
plt.show()

# %%
# Combine with individuals scores
indVA_SCORES = pd.read_csv("indVA_SCORES.csv")

clustered_LOF_scores = pd.concat([indVA_SCORES, bsnVA_SCORES], axis=0, ignore_index=True)

clustered_LOF_scores.to_csv("clustered_LOF_scores.csv", index=False)
clustered_LOF_scores.head()
# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(all_lof_scores, bins=100, edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of Raw LOF Scores (All Clusters)")
plt.grid(True)
plt.show()
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(bsnVA_SCORES["within_cluster_extremeness"], bins=100, edgecolor="black")
plt.xlabel("Within-Cluster Extremeness")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (All BSN Clusters)")
plt.grid(True)
plt.show()

# %%
