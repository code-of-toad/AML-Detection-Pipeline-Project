# %%
# --------------------------------------------------------------
# Dependecies
# --------------------------------------------------------------
from sklearn.ensemble import IsolationForest

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
# For now (March 31st 2:22am), as long as within_clustering.py and within_ind_cluster.py 
# is run before this one, we can just pull ind1_vAF.to_csv("cluster_csvs/ind1.csv")
ind1_vAF = pd.read_csv("cluster_csvs/ind1.csv", index_col="customer_id")
ind2_vAF = pd.read_csv("cluster_csvs/ind2.csv", index_col="customer_id")
ind3_vAF = pd.read_csv("cluster_csvs/ind3.csv", index_col="customer_id")
ind4_vAF = pd.read_csv("cluster_csvs/ind4.csv", index_col="customer_id")
ind5_vAF = pd.read_csv("cluster_csvs/ind5.csv", index_col="customer_id")
ind6_vAF = pd.read_csv("cluster_csvs/ind6.csv", index_col="customer_id")




