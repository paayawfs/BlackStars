"""
Ghana Black Stars Analysis Script
Runnable version of Notebook 04 with correct column names
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Column name mapping for FBref data
PLAYER_COL = 'Player'
SQUAD_COL = 'Squad'
LEAGUE_COL = '_league'

# Ghana Black Stars Forwards
GHANA_PLAYERS = {
    "Mohammed Kudus": ["Kudus", "M. Kudus", "Mohammed Kudus"],
    "Antoine Semenyo": ["Semenyo", "A. Semenyo", "Antoine Semenyo"],
    "Jordan Ayew": ["J. Ayew", "Jordan Ayew", "Ayew"],
    "Ernest Nuamah": ["Nuamah", "E. Nuamah", "Ernest Nuamah"],
    "Osman Bukari": ["Bukari", "O. Bukari", "Osman Bukari"],
    "Fatawu Issahaku": ["Fatawu", "Abdul Fatawu", "A. Fatawu", "Fatawu Issahaku", "Abdul Fatawu Issahaku"],
    "Kamaldeen Sulemana": ["Kamaldeen", "K. Sulemana", "Kamaldeen Sulemana"],
    "Ibrahim Osman": ["I. Osman", "Ibrahim Osman"],
    "Brandon Thomas-Asante": ["Thomas-Asante", "B. Thomas-Asante", "Brandon Thomas-Asante"],
    "Iñaki Williams": ["Inaki Williams", "I. Williams", "Iñaki Williams", "Williams"],
    "Joseph Paintsil": ["Paintsil", "J. Paintsil", "Joseph Paintsil"],
    "Jerry Afriyie": ["Afriyie", "J. Afriyie", "Jerry Afriyie"],
    "Christopher Bonsu Baah": ["Bonsu Baah", "C. Bonsu Baah", "Christopher Bonsu Baah"]
}


def find_player(df, name, aliases):
    """Find a player by name or aliases"""
    all_names = [name] + aliases
    
    for search_name in all_names:
        # Try exact match first
        mask = df[PLAYER_COL].astype(str).str.lower() == search_name.lower()
        if mask.any():
            return df[mask]
        
        # Try contains
        mask = df[PLAYER_COL].astype(str).str.lower().str.contains(search_name.lower(), na=False)
        if mask.any():
            return df[mask]
    
    return pd.DataFrame()


def main():
    print("\n" + "="*60)
    print("🇬🇭 GHANA BLACK STARS ANALYSIS")
    print("="*60)
    
    # Load data
    data_file = PROCESSED_DIR / "forwards_clustered.csv"
    if not data_file.exists():
        print(f"❌ File not found: {data_file}")
        print("   Run Notebook 03 first!")
        return
    
    df = pd.read_csv(data_file)
    print(f"\n✅ Loaded {len(df)} unique forwards")
    
    # Load cluster names
    model_file = OUTPUT_DIR / "clustering_model.pkl"
    if model_file.exists():
        with open(model_file, 'rb') as f:
            model_data = pickle.load(f)
        cluster_names = model_data.get('cluster_names', {})
    else:
        cluster_names = {i: f"Cluster {i}" for i in range(10)}
    
    # Find Ghana players
    print("\n🔍 Searching for Ghana players...\n")
    
    ghana_rows = []
    found_players = []
    not_found_players = []
    
    for canonical_name, aliases in GHANA_PLAYERS.items():
        result = find_player(df, canonical_name, aliases)
        
        if not result.empty:
            result = result.copy()
            result['ghana_name'] = canonical_name
            ghana_rows.append(result.iloc[[0]])  # Take first match only
            found_players.append(canonical_name)
            
            cluster_id = result['cluster'].iloc[0]
            cluster_name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
            team = result[SQUAD_COL].iloc[0]
            league = result.get(LEAGUE_COL, pd.Series([''])).iloc[0]
            
            print(f"  ✅ {canonical_name}")
            print(f"     → {team}, {league}")
            print(f"     → {cluster_name}")
        else:
            not_found_players.append(canonical_name)
            print(f"  ❌ {canonical_name} - NOT FOUND")
    
    if not ghana_rows:
        print("\n❌ No Ghana players found!")
        return
    
    ghana_df = pd.concat(ghana_rows, ignore_index=True)
    ghana_df['cluster_name'] = ghana_df['cluster'].map(cluster_names)
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 FOUND: {len(found_players)}/{len(GHANA_PLAYERS)} players")
    print("="*60)
    
    if not_found_players:
        print(f"\n❌ Not in dataset (need more minutes or different league):")
        for p in not_found_players:
            print(f"   - {p}")
    
    # Squad composition
    print("\n" + "="*60)
    print("🏆 SQUAD COMPOSITION BY PLAYER TYPE")
    print("="*60)
    
    composition = ghana_df.groupby(['cluster', 'cluster_name']).size().reset_index(name='count')
    composition = composition.sort_values('count', ascending=False)
    
    for _, row in composition.iterrows():
        players_in_cluster = ghana_df[ghana_df['cluster'] == row['cluster']]['ghana_name'].tolist()
        print(f"\n{row['cluster_name']}: {row['count']} players")
        for p in players_in_cluster:
            print(f"   • {p}")
    
    # Gap analysis
    print("\n" + "="*60)
    print("🔍 GAP ANALYSIS")
    print("="*60)
    
    all_clusters = set(cluster_names.keys())
    ghana_clusters = set(ghana_df['cluster'].unique())
    missing_clusters = all_clusters - ghana_clusters
    
    if missing_clusters:
        print("\n❌ MISSING PLAYER TYPES:")
        for c in missing_clusters:
            print(f"   • {cluster_names.get(c, f'Cluster {c}')}")
    
    # Save results
    output_file = OUTPUT_DIR / "ghana_analysis.csv"
    ghana_df.to_csv(output_file, index=False)
    print(f"\n💾 Saved: {output_file}")
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
