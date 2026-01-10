"""
K-Means Clustering Engine for Player Role Identification
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import pickle

import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import PROCESSED_DATA_DIR, OUTPUT_DIR, N_CLUSTERS_RANGE


def load_processed_data() -> pd.DataFrame:
    """Load the processed forwards data"""
    filepath = f"{PROCESSED_DATA_DIR}/forwards_processed.csv"
    
    if not Path(filepath).exists():
        print(f"✗ Processed data not found at {filepath}")
        print("  Run processor.py first!")
        return pd.DataFrame()
    
    df = pd.read_csv(filepath)
    print(f"✓ Loaded {len(df)} forwards from processed data")
    return df


def select_clustering_features(df: pd.DataFrame) -> tuple:
    """Select features for clustering"""
    # Core features for clustering
    feature_candidates = [
        # Finishing
        'goals_per90', 'npxg_per90', 'shots_per90', 'sot_per90',
        # Creativity  
        'xag_per90', 'key_passes_per90', 'sca_per90', 'gca_per90',
        # Progression
        'progressive_carries_per90', 'progressive_passes_received_per90',
        # Retention (inverted)
        'dispossessed_per90', 'miscontrols_per90',
        # Physicality
        'aerials_won_per90'
    ]
    
    # Use only features that exist
    available_features = [f for f in feature_candidates if f in df.columns]
    
    if not available_features:
        # Fallback to any numeric columns with 'per90' or normalized
        available_features = [col for col in df.columns 
                            if 'per90' in col.lower() or col.endswith('_norm')]
    
    print(f"✓ Using {len(available_features)} features for clustering:")
    for f in available_features:
        print(f"    - {f}")
    
    return df[available_features].fillna(0), available_features


def find_optimal_clusters(X: pd.DataFrame) -> int:
    """Use elbow method and silhouette score to find optimal k"""
    print("\n" + "="*60)
    print("FINDING OPTIMAL NUMBER OF CLUSTERS")
    print("="*60)
    
    inertias = []
    silhouette_scores = []
    
    for k in N_CLUSTERS_RANGE:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        
        inertias.append(kmeans.inertia_)
        sil_score = silhouette_score(X, kmeans.labels_)
        silhouette_scores.append(sil_score)
        
        print(f"  k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil_score:.3f}")
    
    # Find k with best silhouette score
    best_k = list(N_CLUSTERS_RANGE)[np.argmax(silhouette_scores)]
    print(f"\n✓ Optimal k = {best_k} (best silhouette score)")
    
    return best_k


def run_clustering(df: pd.DataFrame, n_clusters: int) -> tuple:
    """Run K-Means clustering"""
    print("\n" + "="*60)
    print(f"RUNNING K-MEANS CLUSTERING (k={n_clusters})")
    print("="*60)
    
    # Select and scale features
    X, feature_names = select_clustering_features(df)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Run K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add cluster assignments to dataframe
    df['cluster'] = clusters
    
    # Calculate cluster statistics
    print("\nCluster Summary:")
    for i in range(n_clusters):
        cluster_df = df[df['cluster'] == i]
        print(f"\n  Cluster {i}: {len(cluster_df)} players")
        
        # Show top stats for this cluster
        for feat in feature_names[:5]:
            if feat in cluster_df.columns:
                mean_val = cluster_df[feat].mean()
                print(f"    - {feat}: {mean_val:.3f}")
    
    return df, kmeans, scaler, feature_names


def analyze_cluster_profiles(df: pd.DataFrame, feature_names: list) -> dict:
    """Analyze and name clusters based on their characteristics"""
    print("\n" + "="*60)
    print("CLUSTER PROFILE ANALYSIS")
    print("="*60)
    
    cluster_profiles = {}
    
    for cluster_id in df['cluster'].unique():
        cluster_df = df[df['cluster'] == cluster_id]
        
        # Calculate z-scores compared to overall mean
        profile = {}
        for feat in feature_names:
            if feat in cluster_df.columns:
                cluster_mean = cluster_df[feat].mean()
                overall_mean = df[feat].mean()
                overall_std = df[feat].std()
                
                if overall_std > 0:
                    z_score = (cluster_mean - overall_mean) / overall_std
                else:
                    z_score = 0
                
                profile[feat] = {
                    'mean': cluster_mean,
                    'z_score': z_score
                }
        
        # Sort by z-score to find defining characteristics
        sorted_traits = sorted(profile.items(), 
                              key=lambda x: abs(x[1]['z_score']), 
                              reverse=True)
        
        # Name the cluster based on top traits
        cluster_name = suggest_cluster_name(sorted_traits)
        
        cluster_profiles[cluster_id] = {
            'name': cluster_name,
            'size': len(cluster_df),
            'traits': sorted_traits[:5]
        }
        
        print(f"\n  Cluster {cluster_id}: {cluster_name}")
        print(f"    Size: {len(cluster_df)} players")
        print(f"    Key traits:")
        for trait, vals in sorted_traits[:3]:
            direction = "↑" if vals['z_score'] > 0 else "↓"
            print(f"      {direction} {trait}: z={vals['z_score']:.2f}")
    
    return cluster_profiles


def suggest_cluster_name(traits: list) -> str:
    """Suggest a cluster name based on dominant traits"""
    # Simple heuristic naming
    trait_names = [t[0] for t in traits[:3]]
    trait_zs = [t[1]['z_score'] for t in traits[:3]]
    
    # Check for common archetypes
    if any('goal' in t or 'xg' in t for t in trait_names):
        if any(z > 0.5 for z in trait_zs):
            return "Goal Poacher"
    
    if any('assist' in t or 'xag' in t or 'key' in t for t in trait_names):
        if any(z > 0.5 for z in trait_zs):
            return "Creative Playmaker"
    
    if any('carry' in t or 'progress' in t for t in trait_names):
        if any(z > 0.5 for z in trait_zs):
            return "Ball Carrier"
    
    if any('aerial' in t for t in trait_names):
        if any(z > 0.5 for z in trait_zs):
            return "Target Man"
    
    return "Hybrid Forward"


def save_model(kmeans, scaler, feature_names, cluster_profiles: dict):
    """Save the trained model and metadata"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    model_data = {
        'kmeans': kmeans,
        'scaler': scaler,
        'feature_names': feature_names,
        'cluster_profiles': cluster_profiles
    }
    
    filepath = f"{OUTPUT_DIR}/clustering_model.pkl"
    with open(filepath, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✓ Saved clustering model to {filepath}")


def main():
    """Main clustering pipeline"""
    # Load data
    df = load_processed_data()
    
    if df.empty:
        return
    
    # Find optimal number of clusters
    X, feature_names = select_clustering_features(df)
    optimal_k = find_optimal_clusters(X)
    
    # Run clustering
    df, kmeans, scaler, feature_names = run_clustering(df, optimal_k)
    
    # Analyze cluster profiles
    cluster_profiles = analyze_cluster_profiles(df, feature_names)
    
    # Save results
    output_file = f"{PROCESSED_DATA_DIR}/forwards_clustered.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved clustered data to {output_file}")
    
    # Save model
    save_model(kmeans, scaler, feature_names, cluster_profiles)
    
    print("\n✓ Clustering complete!")


if __name__ == "__main__":
    main()
