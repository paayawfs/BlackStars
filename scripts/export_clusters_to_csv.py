"""
Export all players organized by cluster to a CSV file.
"""

import pandas as pd
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    # Load clustered data
    data_file = PROCESSED_DIR / "forwards_clustered.csv"
    
    if not data_file.exists():
        print(f"[ERROR] File not found: {data_file}")
        print("   Run Notebook 03 (clustering) first!")
        return
    
    df = pd.read_csv(data_file)
    print(f"[OK] Loaded {len(df)} players")
    
    # Select key columns for export
    key_columns = [
        'Player', 'Squad', 'Pos', 'Age', 'Nation',
        'Playing Time_90s', 'cluster', 'cluster_name',
        'Performance_Gls_per90', 'Performance_Ast_per90',
        'Expected_xG_per90', 'Expected_xAG_per90',
        'Standard_Sh_per90', 'Take-Ons_Succ_per90',
        'Progression_PrgC_per90', 'SCA_SCA_per90'
    ]
    
    # Use only available columns
    available_cols = [c for c in key_columns if c in df.columns]
    
    # Sort by cluster, then by goals per 90 within each cluster
    sort_col = 'Performance_Gls_per90' if 'Performance_Gls_per90' in df.columns else 'cluster'
    df_sorted = df[available_cols].sort_values(
        by=['cluster', sort_col], 
        ascending=[True, False]
    )
    
    # Export to CSV
    output_file = OUTPUT_DIR / "players_by_cluster.csv"
    df_sorted.to_csv(output_file, index=False)
    print(f"[SAVED] {output_file}")
    
    # Print summary
    print("\nCLUSTER SUMMARY:")
    print("-" * 50)
    for cluster_id in sorted(df['cluster'].unique()):
        cluster_df = df[df['cluster'] == cluster_id]
        cluster_name = cluster_df['cluster_name'].iloc[0] if 'cluster_name' in cluster_df.columns else f"Cluster {cluster_id}"
        print(f"\nCluster {cluster_id}: {len(cluster_df)} players")
        print(f"  {cluster_name}")
        
        # Show top 3 players by goals
        if 'Performance_Gls_per90' in cluster_df.columns:
            top3 = cluster_df.nlargest(3, 'Performance_Gls_per90')
            for _, p in top3.iterrows():
                print(f"    - {p['Player']} ({p['Squad']}) - {p['Performance_Gls_per90']:.2f} G/90")

if __name__ == "__main__":
    main()
