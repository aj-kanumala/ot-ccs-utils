# Import necessary libraries
import numpy as np

# Original Nystrom completion
def nystrom_completion(X, num_cols):
    C = X[:,num_cols]
    U = X[np.ix_(num_cols,num_cols)]
    return C@np.linalg.pinv(U)@C.T


# Rank-Enforced Nystrom completion
def nystrom_completion_rank(X, num_cols, rank):
    C = X[:,num_cols]
    U = X[np.ix_(num_cols,num_cols)]
    u, s, vt = np.linalg.svd(U, full_matrices=False)
    U_pinv = (vt[:rank,:]).T @ np.diag(1/s[:rank]) @ (u[:,:rank]).T
    return C@U_pinv@C.T