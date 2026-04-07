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
individuals_vA = pd.read_csv(
    "/Users/dangernoodle_/Desktop/DATA/DataTables/individuals_vA_2.csv")
ind_VA_FAMD = pd.read_csv(
    "/Users/dangernoodle_/Desktop/DATA/DataTables/VersionA_Individual_AfterFAMD_2.csv")

# 1) Hard checks
if len(individuals_vA) != len(ind_VA_FAMD):
    raise ValueError(f"Row count mismatch: customers={len(individuals_vA)} famd={len(ind_VA_FAMD)}")

if "customer_id" not in individuals_vA.columns:
    raise ValueError("customers CSV must contain customer_id")

# 2) Attach by position safely
indVA_FAMD_output = ind_VA_FAMD.copy()
indVA_FAMD_output.insert(0, "customer_id", individuals_vA["customer_id"].to_numpy())
indVA_FAMD_output.insert(1, "cluster", individuals_vA["cluster"].to_numpy())

# 3) Optional: assert uniqueness
if indVA_FAMD_output["customer_id"].duplicated().any():
    raise ValueError("customer_id is not unique in customers_business_only.csv (unexpected for a key).")

indVA_FAMD_output.to_csv("famd_with_customer_id.csv", index=False)

# %%
# --------------------------------------------------------------
# MAKING SUBSETS BY CLUSTER GROUPING
# --------------------------------------------------------------

# CLUSTER 6 BC-BASED ACTIVE CUSTOMERS
ind6_vAF = indVA_FAMD_output[indVA_FAMD_output["cluster"] == "individual_6"]

# Dropping cluster type column
ind6_vAF = ind6_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
ind6_vAF_copy = ind6_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
ind6_vAF = ind6_vAF.set_index("customer_id", drop=True)
ind6_vAF.to_csv("cluster_csvs/ind6.csv")
#dfind6_vAF = ind6_vAF.reset_index() to put back

# %%
# --------------------------------------------------------------
# LOCAL OUTLIER FACTOR first trial
# --------------------------------------------------------------

ind6_lof_model = LocalOutlierFactor(
    n_neighbors=60,
    contamination=0.041837,
    n_jobs=-1
    )

ind6_lof_fitted = ind6_lof_model.fit_predict(ind6_vAF)

ind6_lof_scores = pd.Series(
    ind6_lof_model.negative_outlier_factor_,
    index=ind6_vAF.index)

ind6_scored = ind6_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
ind6_scored.loc[ind6_lof_scores.index, "lof_score_raw"] = ind6_lof_scores

lof_all_norm = normalize_to_unit_interval(ind6_lof_scores)

df_out_ind6 = (
    pd.DataFrame({
        "customer_id": ind6_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": ind6_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_ind6 = df_out_ind6[["customer_id", "outlier_score_01"]]

df_out_ind6.to_csv("ind6_LOF_k60_score.csv", index=False,
              float_format="%.10f")

top_ids = ind6_lof_scores.sort_values(ascending=True).index
top_anomalies_ind6 = ind6_scored.loc[top_ids].copy()
top_anomalies_ind6.to_csv("ind6_LOF_k60.csv", index=False)

# %%
# --------------------------------------------------------------
# LOCAL OUTLIER FACTOR LOOP
# --------------------------------------------------------------
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "within_cluster_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ks = list(range(10, 200, 5))

TOP_N = 1309

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

rank_by_k = {}

for k in ks:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination=0.041837,
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(ind6_vAF)

    lof_scores = pd.Series(
        lof_loop.negative_outlier_factor_,
        index=ind6_vAF.index,
        name="lof_score_raw"
    )

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the ind6 table that has customer_id as a column
    ind6_scored_k = ind6_vAF_copy.copy()
    ind6_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N).index
    top_anomalies_k = ind6_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
        os.path.join(OUTPUT_DIR, f"ind6_LOF_top{TOP_N}_k{k}.csv"),
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
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_ind6_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(100, 0) #to change sclae of y-axis
plt.title("LOF (ind6): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(ind6_lof_scores, bins=int(np.sqrt(len(ind6_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (IND6)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(ind6_lof_scores)

ind6_lof_final = (
    pd.DataFrame({
        "customer_id": ind6_lof_scores.index,
        "outlier_score_01": lof_scaled,
        "lof_score_raw": ind6_lof_scores.values
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

ind6_lof_final = ind6_lof_final[["customer_id", "outlier_score_01"]]

ind6_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "ind6_LOF_k60_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (IND6 n = 1309)")
plt.grid(True)
plt.show()


# %%
# --------------------------------------------------------------
# MAKING SUBSETS BY CLUSTER GROUPING
# --------------------------------------------------------------

# CLUSTER 5 --------------------------------------------------------------
ind5_vAF = indVA_FAMD_output[indVA_FAMD_output["cluster"] == "individual_5"]

# Dropping cluster type column
ind5_vAF = ind5_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
ind5_vAF_copy = ind5_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
ind5_vAF = ind5_vAF.set_index("customer_id", drop=True)
ind5_vAF.to_csv("cluster_csvs/ind5.csv")
#dfind5_vAF = ind5_vAF.reset_index() to put back

# CLUSTER 4 --------------------------------------------------------------
ind4_vAF = indVA_FAMD_output[indVA_FAMD_output["cluster"] == "individual_4"]

# Dropping cluster type column
ind4_vAF = ind4_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
ind4_vAF_copy = ind4_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
ind4_vAF = ind4_vAF.set_index("customer_id", drop=True)
ind4_vAF.to_csv("cluster_csvs/ind4.csv")
#dfind4_vAF = ind4_vAF.reset_index() to put back

# CLUSTER 3 -------------------------------------------------------------
ind3_vAF = indVA_FAMD_output[indVA_FAMD_output["cluster"] == "individual_3"]

# Dropping cluster type column
ind3_vAF = ind3_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
ind3_vAF_copy = ind3_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
ind3_vAF = ind3_vAF.set_index("customer_id", drop=True)
ind3_vAF.to_csv("cluster_csvs/ind3.csv")
#dfind3_vAF = ind3_vAF.reset_index() to put back

# CLUSTER 2 -------------------------------------------------------------
ind2_vAF = indVA_FAMD_output[indVA_FAMD_output["cluster"] == "individual_2"]

# Dropping cluster type column
ind2_vAF = ind2_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
ind2_vAF_copy = ind2_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
ind2_vAF = ind2_vAF.set_index("customer_id", drop=True)
ind2_vAF.to_csv("cluster_csvs/ind2.csv")
#dfind2_vAF = ind2_vAF.reset_index() to put back

# CLUSTER 1 -------------------------------------------------------------
ind1_vAF = indVA_FAMD_output[indVA_FAMD_output["cluster"] == "individual_1"]

# Dropping cluster type column
ind1_vAF = ind1_vAF.drop(columns=["cluster"])

# Keeping customer id as index AND column for reattaching
ind1_vAF_copy = ind1_vAF.set_index("customer_id", drop=False)

# Setting customer id as index
ind1_vAF = ind1_vAF.set_index("customer_id", drop=True)
ind1_vAF.to_csv("cluster_csvs/ind1.csv")
#dfind1_vAF = ind1_vAF.reset_index() to put back

# %%
# --------------------------------------------------------------
# CLUSTER 5 FIRST FIT
# --------------------------------------------------------------
# 4392 rows
ind5_lof_model = LocalOutlierFactor(
    n_neighbors=350,
    contamination=.02,
    n_jobs=-1
    )

ind5_lof_fitted = ind5_lof_model.fit_predict(ind5_vAF)

ind5_lof_scores = pd.Series(
    ind5_lof_model.negative_outlier_factor_,
    index=ind5_vAF.index)

ind5_scored = ind5_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
ind5_scored.loc[ind5_lof_scores.index, "lof_score_raw"] = ind5_lof_scores

lof_all_norm = normalize_to_unit_interval(ind5_lof_scores)

df_out_ind5 = (
    pd.DataFrame({
        "customer_id": ind5_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": ind5_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_ind5 = df_out_ind5[["customer_id", "outlier_score_01"]]

df_out_ind5.to_csv("ind5_LOF_k350_score.csv", index=False,
              float_format="%.10f")

top_ids = ind5_lof_scores.sort_values(ascending=True).index
top_anomalies_ind5 = ind5_scored.loc[top_ids].copy()
top_anomalies_ind5.to_csv("ind5_LOF_k350.csv", index=False)


pd.read_csv("ind5_LOF_k350.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 5 LOOP
# --------------------------------------------------------------
k5 = list(range(200, 400, 10))

TOP_N_k5 = 14509 

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
rank_by_k = {}

for k in k5:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination=.02,
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(ind5_vAF)

    lof_scores = pd.Series(
        lof_loop.negative_outlier_factor_,
        index=ind5_vAF.index,
        name="lof_score_raw"
    )

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the ind5 table that has customer_id as a column
    ind5_scored_k = ind5_vAF_copy.copy()
    ind5_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k5).index
    top_anomalies_k = ind5_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
        os.path.join(OUTPUT_DIR, f"ind5_LOF_top{TOP_N_k5}_k{k}.csv"),
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
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_ind5_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(50, 0) #to change sclae of y-axis
plt.title("LOF (ind5): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(ind5_lof_scores, bins=int(np.sqrt(len(ind5_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (IND5)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(ind5_lof_scores)

ind5_lof_final = (
    pd.DataFrame({
        "customer_id": ind5_lof_scores.index,
        "outlier_score_01": lof_scaled,
        "lof_score_raw": ind5_lof_scores.values
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

ind5_lof_final = ind5_lof_final[["customer_id", "outlier_score_01"]]

ind5_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "ind5_LOF_k350_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (IND5 n = 14509)")
plt.grid(True)
plt.show()






# %%
# --------------------------------------------------------------
# CLUSTER 4 FIRST FIT
# --------------------------------------------------------------
# 3892 rows
ind4_lof_model = LocalOutlierFactor(
    n_neighbors=30,
    contamination=.05,
    n_jobs=-1
    )

ind4_lof_fitted = ind4_lof_model.fit_predict(ind4_vAF)

ind4_lof_scores = pd.Series(
    ind4_lof_model.negative_outlier_factor_,
    index=ind4_vAF.index)

ind4_scored = ind4_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
ind4_scored.loc[ind4_lof_scores.index, "lof_score_raw"] = ind4_lof_scores

lof_all_norm = normalize_to_unit_interval(ind4_lof_scores)

df_out_ind4 = (
    pd.DataFrame({
        "customer_id": ind4_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": ind4_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_ind4 = df_out_ind4[["customer_id", "outlier_score_01"]]

df_out_ind4.to_csv("ind4_LOF_k30_score.csv", index=False,
              float_format="%.10f")

top_ids = ind4_lof_scores.sort_values(ascending=True).index
top_anomalies_ind4 = ind4_scored.loc[top_ids].copy()
top_anomalies_ind4.to_csv("ind4_LOF_k30.csv", index=False)


pd.read_csv("ind4_LOF_k30.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 4 LOOP
# --------------------------------------------------------------
k4 = list(range(10, 200, 10))

TOP_N_k4 = 3892

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

rank_by_k = {}

for k in k4:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(ind4_vAF)

    lof_scores = pd.Series(
        lof_loop.negative_outlier_factor_,
        index=ind4_vAF.index,
        name="lof_score_raw"
    )

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the ind4 table that has customer_id as a column
    ind4_scored_k = ind4_vAF_copy.copy()
    ind4_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k4).index
    top_anomalies_k = ind4_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
        os.path.join(OUTPUT_DIR, f"ind4_LOF_top{TOP_N_k4}_k{k}.csv"),
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
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_ind4_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.ylim(50, 0) #to change sclae of y-axis
plt.title("LOF (ind4): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(ind4_lof_scores, bins=int(np.sqrt(len(ind4_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (IND4)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(ind4_lof_scores)

ind4_lof_final = (
    pd.DataFrame({
        "customer_id": ind4_lof_scores.index,
        "outlier_score_01": lof_scaled,
        "lof_score_raw": ind4_lof_scores.values
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

ind4_lof_final = ind4_lof_final[["customer_id", "outlier_score_01"]]

ind4_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "ind4_LOF_k30_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (IND4 n = 3892)")
plt.grid(True)
plt.show()






# %%
# --------------------------------------------------------------
# CLUSTER 3 FIRST FIT
# --------------------------------------------------------------
# 15659 rows
ind3_lof_model = LocalOutlierFactor(
    n_neighbors=475,
    contamination=.05,
    n_jobs=-1
    )

ind3_lof_fitted = ind3_lof_model.fit_predict(ind3_vAF)

ind3_lof_scores = pd.Series(
    ind3_lof_model.negative_outlier_factor_,
    index=ind3_vAF.index
)

ind3_scored = ind3_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
ind3_scored.loc[ind3_lof_scores.index, "lof_score_raw"] = ind3_lof_scores

lof_all_norm = normalize_to_unit_interval(ind3_lof_scores)

df_out_ind3 = (
    pd.DataFrame({
        "customer_id": ind3_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": ind3_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_ind3 = df_out_ind3[["customer_id", "outlier_score_01"]]

df_out_ind3.to_csv("ind3_LOF_k475_score.csv", index=False,
              float_format="%.10f")

top_ids = ind3_lof_scores.sort_values(ascending=True).index
top_anomalies_ind3 = ind3_scored.loc[top_ids].copy()
top_anomalies_ind3.to_csv("ind3_LOF_k475.csv", index=False)

pd.read_csv("ind3_LOF_k475.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 3 LOOP
# --------------------------------------------------------------
k3 = list(range(100, 800, 20))

TOP_N_k3 = 15659

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

rank_by_k = {}

for k in k3:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(ind3_vAF)

    lof_scores = pd.Series(
    lof_loop.negative_outlier_factor_,
    index=ind3_vAF.index,
    name="lof_score_raw"
)

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the ind3 table that has customer_id as a column
    ind3_scored_k = ind3_vAF_copy.copy()
    ind3_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k3).index
    top_anomalies_k = ind3_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
    os.path.join(OUTPUT_DIR, f"ind3_LOF_top{TOP_N_k3}_k{k}.csv"),
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
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_ind3_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
plt.ylim(20, 0)
plt.title("LOF (IND3 n = 15399): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(ind3_lof_scores, bins=int(np.sqrt(len(ind3_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (IND3)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(ind3_lof_scores)

ind3_lof_final = (
    pd.DataFrame({
        "customer_id": ind3_lof_scores.index,
        "outlier_score_01": lof_scaled,
        "lof_score_raw": ind3_lof_scores.values
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

ind3_lof_final = ind3_lof_final[["customer_id", "outlier_score_01"]]

ind3_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "ind3_LOF_k475_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (IND3 n = 15659)")
plt.grid(True)
plt.show()





# %%
# --------------------------------------------------------------
# CLUSTER 2 FIRST FIT
# --------------------------------------------------------------
# 15886 rows
ind2_lof_model = LocalOutlierFactor(
    n_neighbors=775,
    contamination=.01,
    n_jobs=-1
    )

ind2_lof_fitted = ind2_lof_model.fit_predict(ind2_vAF)

ind2_lof_scores = pd.Series(
    ind2_lof_model.negative_outlier_factor_,
    index=ind2_vAF.index
)

ind2_scored = ind2_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
ind2_scored.loc[ind2_lof_scores.index, "lof_score_raw"] = ind2_lof_scores

lof_all_norm = normalize_to_unit_interval(ind2_lof_scores)

df_out_ind2 = (
    pd.DataFrame({
        "customer_id": ind2_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": ind2_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_ind2 = df_out_ind2[["customer_id", "outlier_score_01"]]

df_out_ind2.to_csv("ind2_LOF_k775_score.csv", index=False,
              float_format="%.10f")

top_ids = ind2_lof_scores.sort_values(ascending=True).index
top_anomalies_ind2 = ind2_scored.loc[top_ids].copy()
top_anomalies_ind2.to_csv("ind2_LOF_top.csv", index=False)

pd.read_csv("ind2_LOF_top.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 2 LOOP
# --------------------------------------------------------------
k2 = list(range(400, 900, 50))

TOP_N_k2 = 15886

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

rank_by_k = {}

for k in k2:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination=.01,
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(ind2_vAF)

    lof_scores = pd.Series(
    lof_loop.negative_outlier_factor_,
    index=ind2_vAF.index,
    name="lof_score_raw"
)

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the ind2 table that has customer_id as a column
    ind2_scored_k = ind2_vAF_copy.copy()
    ind2_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k2).index
    top_anomalies_k = ind2_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
    os.path.join(OUTPUT_DIR, f"ind2_LOF_top{TOP_N_k2}_k{k}.csv"),
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
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_ind2_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(20, 0)
plt.title("LOF (ind2): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(ind2_lof_scores, bins=int(np.sqrt(len(ind2_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (IND2)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(ind2_lof_scores)

ind2_lof_final = (
    pd.DataFrame({
        "customer_id": ind2_lof_scores.index,
        "outlier_score_01": lof_scaled,
        "lof_score_raw": ind2_lof_scores.values
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

ind2_lof_final = ind2_lof_final[["customer_id", "outlier_score_01"]]

ind2_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "ind2_LOF_k775_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (IND2 n = 15886)")
plt.grid(True)
plt.show()






# %%
# --------------------------------------------------------------
# CLUSTER 1 FIRST FIT
# --------------------------------------------------------------
# 1844 rows
ind1_lof_model = LocalOutlierFactor(
    n_neighbors=100,
    contamination=.02,
    n_jobs=-1
    )

ind1_lof_fitted = ind1_lof_model.fit_predict(ind1_vAF)

ind1_lof_scores = pd.Series(
    ind1_lof_model.negative_outlier_factor_,
    index=ind1_vAF.index
)

ind1_scored = ind1_vAF_copy.copy()  # has customer_id column and is indexed by customer_id
ind1_scored.loc[ind1_lof_scores.index, "lof_score_raw"] = ind1_lof_scores

lof_all_norm = normalize_to_unit_interval(ind1_lof_scores)

df_out_ind1 = (
    pd.DataFrame({
        "customer_id": ind1_lof_scores.index,
        "outlier_score_01": lof_all_norm.values,
        "lof_score_raw": ind1_lof_scores.values,
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

df_out_ind1 = df_out_ind1[["customer_id", "outlier_score_01"]]

df_out_ind1.to_csv("ind1_LOF_k204_scores.csv", index=False,
              float_format="%.10f")

top_ids = ind1_lof_scores.sort_values(ascending=True).index
top_anomalies_ind1 = ind1_scored.loc[top_ids].copy()
top_anomalies_ind1.to_csv("ind1_LOF_top.csv", index=False)

pd.read_csv("ind1_LOF_top.csv").head()

# %%
# --------------------------------------------------------------
# CLUSTER 1 LOOP
# --------------------------------------------------------------
k1 = list(range(20, 300, 5))

TOP_N_k1 = 1844

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

rank_by_k = {}

for k in k1:
    lof_loop = LocalOutlierFactor(
        n_neighbors=k,
        contamination="auto",
        n_jobs=-1
    )

    _ = lof_loop.fit_predict(ind1_vAF)

    lof_scores = pd.Series(
    lof_loop.negative_outlier_factor_,
    index=ind1_vAF.index,
    name="lof_score_raw"
)

    # ranks for movement plot (1 = most outlier; most negative LOF = strongest outlier)
    rank_by_k[k] = lof_scores.rank(method="min", ascending=True).astype(int)

    # attach scores to a copy of the ind1 table that has customer_id as a column
    ind1_scored_k = ind1_vAF_copy.copy()
    ind1_scored_k.loc[lof_scores.index, "lof_score_raw"] = lof_scores

    # export top anomalies for this k
    top_ids = lof_scores.nsmallest(TOP_N_k1).index
    top_anomalies_k = ind1_scored_k.loc[top_ids].copy()
    top_anomalies_k.to_csv(
    os.path.join(OUTPUT_DIR, f"ind1_LOF_top{TOP_N_k1}_k{k}.csv"),
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
    os.path.join(OUTPUT_DIR, "tracked_rank_movement_ind1_LOF.csv"),
    index=False
)

plt.figure()
for cid, g in tracked.groupby("customer_id"):
    plt.plot(g["k"], g["rank"], marker="o", markersize=2, label=str(cid))
plt.gca().invert_yaxis()
plt.xlabel("n_neighbors (k)")
plt.ylabel("Rank (1 = most outlier)")
#plt.ylim(30, 0)
plt.title("LOF (IND1 n = 14516): rank movement across k")
plt.grid(True)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()

# %%
# PLOT OF RAW SCORES
plt.figure()
plt.hist(ind1_lof_scores, bins=int(np.sqrt(len(ind1_lof_scores))), edgecolor="black")
plt.xlabel("LOF Score (negative_outlier_factor_)")
plt.ylabel("Count")
plt.title("Distribution of LOF Scores (IND1)")
plt.grid(True)
plt.show()
# %%
lof_scaled = normalize_to_unit_interval(ind1_lof_scores)

ind1_lof_final = (
    pd.DataFrame({
        "customer_id": ind1_lof_scores.index,
        "outlier_score_01": lof_scaled,
        "lof_score_raw": ind1_lof_scores.values
    })
    .sort_values(["outlier_score_01", "lof_score_raw"], ascending=[False, True])
)

ind1_lof_final = ind1_lof_final[["customer_id", "outlier_score_01"]]

ind1_lof_final.to_csv(
    os.path.join("within_cluster_outputs", "ind1_LOF_k100_score.csv"),
    index=False,
    float_format="%.6f"
)
# %%
# PLOT OF NORMALIZED SCORES
plt.figure()
plt.hist(lof_scaled, bins=int(np.sqrt(len(lof_scaled))), edgecolor="black")
plt.xlabel("Normalized LOF Score")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (IND1 n = 1844)")
plt.grid(True)
plt.show()



# %%
# --------------------------------------------------------------
# SCORES ONLY FOR RULE BASED ALGO
# --------------------------------------------------------------

# Combine all raw LOF scores across clusters into one Series
all_lof_scores = pd.concat([
    ind1_lof_scores,
    ind2_lof_scores,
    ind3_lof_scores,
    ind4_lof_scores,
    ind5_lof_scores,
    ind6_lof_scores
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

top_anomalies_ind1 = compute_global_extremeness(top_anomalies_ind1, ind1_lof_scores)
top_anomalies_ind2 = compute_global_extremeness(top_anomalies_ind2, ind2_lof_scores)
top_anomalies_ind3 = compute_global_extremeness(top_anomalies_ind3, ind3_lof_scores)
top_anomalies_ind4 = compute_global_extremeness(top_anomalies_ind4, ind4_lof_scores)
top_anomalies_ind5 = compute_global_extremeness(top_anomalies_ind5, ind5_lof_scores)
top_anomalies_ind6 = compute_global_extremeness(top_anomalies_ind6, ind6_lof_scores)

# %%
indVA_SCORES = pd.concat([
    top_anomalies_ind1[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_ind2[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_ind3[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_ind4[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_ind5[["customer_id", "within_cluster_extremeness"]],
    top_anomalies_ind6[["customer_id", "within_cluster_extremeness"]]
], axis=0, ignore_index=True)

indVA_SCORES.to_csv("indVA_SCORES.csv", index=False)
indVA_SCORES.head()
# %%
indVA_SCORES.to_csv("indVA_SCORES.csv", index=False)

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
plt.hist(indVA_SCORES["within_cluster_extremeness"], bins=100, edgecolor="black")
plt.xlabel("Within-Cluster Extremeness")
plt.ylabel("Count")
plt.title("Distribution of Normalized LOF Scores (All Clusters)")
plt.grid(True)
plt.show()
# %%
ind_lof_all = pd.concat([
    ind1_lof_final,
    ind2_lof_final,
    ind3_lof_final,
    ind4_lof_final,
    ind5_lof_final,
    ind6_lof_final
], axis=0, ignore_index=True)

plt.figure()
plt.hist(ind_lof_all["outlier_score_01"], bins=100, edgecolor="black")
plt.xlabel("Normalized LOF Score (within-cluster scaled)")
plt.ylabel("Count")
plt.title("Distribution of Within-Cluster Scaled LOF Scores (All Clusters)")
plt.grid(True)
plt.show()
# %%
comparison = ind_lof_all[["customer_id", "outlier_score_01"]].merge(
    indVA_SCORES[["customer_id", "within_cluster_extremeness"]],
    on="customer_id"
)

plt.figure()
plt.scatter(comparison["outlier_score_01"], comparison["within_cluster_extremeness"], 
            alpha=0.3, s=5)
plt.xlabel("Within-Cluster Scaled Score (ind#_lof_final)")
plt.ylabel("Global Extremeness Score (indVA_SCORES)")
plt.title("Within-Cluster Scaled vs Global Extremeness")
plt.grid(True)
plt.show()
# %%
comparison["rank_within"] = comparison["outlier_score_01"].rank(ascending=False)
comparison["rank_global"] = comparison["within_cluster_extremeness"].rank(ascending=False)
comparison["rank_diff"] = comparison["rank_within"] - comparison["rank_global"]

# Customers whose rank shifts the most between the two methods
comparison.sort_values("rank_diff", key=abs, ascending=False).head(20)
# better to use global 