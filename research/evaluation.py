# Import necessary libraries
import numpy as np
import pandas as pd
import time

def compute_snr_db(W_true, W_recon):
    """
    Compute SNR (in dB) between ground truth and reconstructed distance matrices.
    """
    signal = np.linalg.norm(W_true)
    noise = np.linalg.norm(W_true - W_recon)
    if noise <= 0:
        return np.inf
    return 20 * np.log10(signal / noise)


# Store SNR values for various p and delta values
def comapare_CCS_SNR(dist_matrix, pd_values_df, method=1, r=4):
    """
    This function takes in a full distance matrix and applies CCS-ICURC algorithm
    Computes Signal to Noise Ratio for various pre-computed p and delta values
    """  
    tot_n = dist_matrix.shape[0]
    pd_values_df["SNR"] = np.nan
    pd_values_df["RecoveryTime(secs)"] = np.nan
    pd_values_df["CCS_Sample%"] = np.nan
    # Iterate through different p and delta values from DataFrame
    for idx, row in pd_values_df.iterrows():
        params_CCS = {'p': row['p'], 'delta': row['delta']}
        #print(params_CCS)
        params_ICURC = {
        'eta': [1 / params_CCS['p'], 1 / params_CCS['p'], 1 / (2 * params_CCS['p'])],
        'TOL': 1e-4,
        'max_ite': 100
        }
        # Apply column-only CCS on the full distance matrix
        X_Omega_CCS, J_CCS, sampled_positions, C_Obs = CCS(dist_matrix, params_CCS)
        #X_Omega_ccs[np.ix_(J_ccs, J_ccs)] = dist_matrix[np.ix_(J_ccs, J_ccs)]
        C, U_pinv, ICURC_time = ICURC(X_Omega_CCS, J_CCS, r, params_ICURC)
        Mout_CURf = C @ U_pinv @ C.T
        np.fill_diagonal(Mout_CURf, 0) 
        ccs_snr = compute_snr_db(dist_matrix, Mout_CURf)  # Compute SNR
        
        # Assign SNR to the current row
        pd_values_df.at[idx, "SNR"] = round(ccs_snr,4)
        pd_values_df.at[idx, "RecoveryTime(secs)"] = round(ICURC_time,2)
        pd_values_df.at[idx, "CCS_Sample%"] = round((len(sampled_positions)/(tot_n*tot_n)*100),2)
        
    return pd_values_df


