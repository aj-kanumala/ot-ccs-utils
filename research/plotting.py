import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap


def visualize_distance_matrix(
        W_partial,
        title="Wasserstein Distance Matrix",
        highlight_color='lime'):          # any matplotlib colour name / hex
    """
    Heat-map:
      • 0          → black
      • non-zero   → single highlight colour (no gradient)
      • no colour-bar
    Args:
        W_partial: np.ndarray of shape [N, N]
        title:     plot title
        highlight_color: colour for non-zero cells
    """
    plt.figure(figsize=(8, 7))
    # 1. Binary mask
    mask_nonzero = (W_partial != 0).astype(float)   # 1.0 = non-zero, 0.0 = zero
    # 2. Plot zeros → black background
    plt.imshow(np.zeros_like(W_partial),
               cmap='gray', vmin=0, vmax=1, interpolation='nearest')
    # Create a colormap that maps 0 → black and 1 → highlight_color
    cmap = ListedColormap(['black', highlight_color])
    plt.imshow(mask_nonzero, cmap=cmap, vmin=0, vmax=1,
               interpolation='nearest', alpha=1.0)

    plt.title(title, fontsize=14)
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    plt.xlabel("Image Index")
    plt.ylabel("Image Index")
    plt.tight_layout()
    plt.show()



def show_snr_lineplot(df_input):
    """ Plots only non-zero and non-null SNR values"""
    #df = df_input.loc[df_input['SNR'] > 0]
    #df = df_input.where(df_input['SNR'] > 0).dropna()
    df=df_input.copy()
    # Create a new column for x-axis labels as (p, delta) pairs
    df['p_delta_pair'] = list(zip(df['p'], df['delta'], df['CCS_Sample%']))  # tuple pairs
    # OR as strings if you want nicer labels: "(p, delta)"
    df['p_delta_pair_str'] = df['p_delta_pair'].apply(lambda x: f"({x[0]:.2f}, {x[1]:.2f}, {x[2]:.1f})")

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(df['p_delta_pair_str'], df['SNR'], marker='o', linestyle='-')
    plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for readability
    plt.xlabel('(p, delta, Sample%)')
    plt.ylabel('SNR (dB)')
    plt.title('SNR for different (p, delta) pairs')
    plt.grid(False)
    plt.tight_layout()
    plt.show()


def rank_snr_lineplot(df_input):
    """ Plots only non-zero and non-null SNR values"""
    #df = df_input.loc[df_input['SNR'] > 0]
    df = df_input.where(df_input['SNR'] > 0).dropna()
    """ Plots all SNR values"""
    #df=df_input.copy()
    # Create a new column for x-axis labels as (p, delta) pairs
    df['p_delta_rank'] = list(zip(df['p'], df['delta'], df['Rank']))  # tuple pairs
    # OR as strings if you want nicer labels: "(p, delta)"
    df['p_delta_pair_str'] = df['p_delta_rank'].apply(lambda x: f"({x[0]:.2f}, {x[1]:.2f}, {x[2]:.1f})")

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(df['p_delta_pair_str'], df['SNR'], marker='o', color='green', linestyle='-')
    plt.xticks(rotation=90, ha='right')  # rotate x-axis labels for readability
    plt.xlabel('(p, delta, Rank)')
    plt.ylabel('SNR (dB)')
    plt.title('SNR for different (p, delta, rank) pairs')
    plt.grid(False)
    plt.tight_layout()
    plt.show()
    

def rank_snr_heatmap(df_input, rounded_frac=True):
    """ Plots only non-zero and non-null SNR values"""
    #df = df_input.where(df_input['SNR'] > 0).dropna()
    """ Plots all SNR values"""
    df=df_input.copy()
    # Create a pivot table for heatmap
    if rounded_frac:
        heatmap_data = df.pivot(index='SamplePercentage', columns='Rank', values='SNR')
    else:
        heatmap_data = df.pivot(index='CCS_Sample%', columns='Rank', values='SNR')    
    plt.figure(figsize=(10,6))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='viridis')
    plt.xlabel('Rank')
    plt.ylabel('Sample Percentage')
    plt.title('SNR Heatmap')
    plt.show()