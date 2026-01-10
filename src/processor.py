"""
Feature Engineering and Data Processing
Normalizes stats and prepares data for clustering
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, METRICS, 
    MIN_MINUTES_PLAYED, FORWARD_POSITIONS
)


def load_raw_data() -> pd.DataFrame:
    """Load all raw CSV files and combine into single DataFrame"""
    raw_path = Path(RAW_DATA_DIR)
    all_dfs = []
    
    # Find all standard stats files (these have the base player info)
    for csv_file in raw_path.glob("*_standard.csv"):
        print(f"Loading: {csv_file.name}")
        df = pd.read_csv(csv_file)
        
        # Extract league and season from filename
        parts = csv_file.stem.split("_")
        # Handle multi-word league names
        if "standard" in parts:
            idx = parts.index("standard")
            season = "_".join(parts[idx-2:idx])
            league = "_".join(parts[:idx-2])
        
        df['source_file'] = csv_file.name
        all_dfs.append(df)
    
    if not all_dfs:
        print("No raw data files found!")
        return pd.DataFrame()
    
    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"\n✓ Loaded {len(combined)} total player records")
    return combined


def load_stat_type(stat_type: str) -> pd.DataFrame:
    """Load all files of a specific stat type"""
    raw_path = Path(RAW_DATA_DIR)
    all_dfs = []
    
    for csv_file in raw_path.glob(f"*_{stat_type}.csv"):
        df = pd.read_csv(csv_file)
        all_dfs.append(df)
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()


def identify_columns(df: pd.DataFrame) -> dict:
    """Identify the actual column names in the DataFrame"""
    col_mapping = {}
    
    # Common column name patterns
    patterns = {
        'player': ['player', 'Player', 'name', 'Name'],
        'team': ['team', 'Team', 'squad', 'Squad'],
        'position': ['pos', 'Pos', 'position', 'Position'],
        'minutes': ['min', 'Min', 'minutes', 'Minutes', '90s'],
        'goals': ['gls', 'Gls', 'goals', 'Goals'],
        'assists': ['ast', 'Ast', 'assists', 'Assists'],
        'xg': ['xg', 'xG', 'expected_goals'],
        'npxg': ['npxg', 'npxG', 'np_xg'],
        'xag': ['xag', 'xAG', 'xa', 'xA'],
    }
    
    for key, possible_names in patterns.items():
        for col in df.columns:
            col_str = str(col).lower()
            for name in possible_names:
                if name.lower() in col_str:
                    col_mapping[key] = col
                    break
            if key in col_mapping:
                break
    
    return col_mapping


def filter_forwards(df: pd.DataFrame, col_mapping: dict) -> pd.DataFrame:
    """Filter to only include forwards/attackers"""
    if 'position' not in col_mapping:
        print("⚠ No position column found, returning all players")
        return df
    
    pos_col = col_mapping['position']
    mask = df[pos_col].astype(str).str.upper().str.contains(
        '|'.join(['FW', 'LW', 'RW', 'ST', 'CF']), 
        na=False
    )
    
    filtered = df[mask].copy()
    print(f"✓ Filtered to {len(filtered)} forwards/attackers")
    return filtered


def deduplicate_players(df: pd.DataFrame, col_mapping: dict) -> pd.DataFrame:
    """Remove duplicate player entries (same Player + Squad combination)"""
    player_col = col_mapping.get('player', 'Player')
    team_col = col_mapping.get('team', 'Squad')
    
    # Find actual column names
    player_col = next((c for c in df.columns if c.lower() == 'player'), player_col)
    team_col = next((c for c in df.columns if c.lower() == 'squad'), team_col)
    
    before_count = len(df)
    
    # Drop duplicates based on Player + Squad, keeping first occurrence
    df = df.drop_duplicates(subset=[player_col, team_col], keep='first')
    
    after_count = len(df)
    removed = before_count - after_count
    
    print(f"✓ Deduplicated: {before_count} → {after_count} players (removed {removed} duplicates)")
    return df


def filter_minimum_minutes(df: pd.DataFrame, col_mapping: dict) -> pd.DataFrame:
    """Filter players with minimum minutes played"""
    if 'minutes' not in col_mapping:
        print("⚠ No minutes column found")
        return df
    
    min_col = col_mapping['minutes']
    
    # Handle if column is '90s' (number of 90-minute periods)
    if '90' in str(min_col).lower():
        mask = df[min_col].astype(float) >= (MIN_MINUTES_PLAYED / 90)
    else:
        mask = df[min_col].astype(float) >= MIN_MINUTES_PLAYED
    
    filtered = df[mask].copy()
    print(f"✓ Filtered to {len(filtered)} players with >={MIN_MINUTES_PLAYED} minutes")
    return filtered


def normalize_per_90(df: pd.DataFrame, col_mapping: dict) -> pd.DataFrame:
    """Convert counting stats to per-90 basis"""
    if 'minutes' not in col_mapping:
        return df
    
    min_col = col_mapping['minutes']
    
    # Calculate 90s played
    if '90' in str(min_col).lower():
        df['90s_played'] = df[min_col].astype(float)
    else:
        df['90s_played'] = df[min_col].astype(float) / 90
    
    # Columns to convert to per-90
    counting_stats = ['goals', 'assists', 'xg', 'npxg', 'xag']
    
    for stat in counting_stats:
        if stat in col_mapping:
            col = col_mapping[stat]
            if col in df.columns:
                new_col = f"{stat}_per90"
                df[new_col] = df[col].astype(float) / df['90s_played'].replace(0, np.nan)
    
    return df


def normalize_features(df: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
    """Apply MinMax scaling to normalize features to 0-1 range"""
    scaler = MinMaxScaler()
    
    # Only scale columns that exist
    existing_cols = [col for col in feature_cols if col in df.columns]
    
    if existing_cols:
        df[existing_cols] = scaler.fit_transform(df[existing_cols].fillna(0))
        print(f"✓ Normalized {len(existing_cols)} features to 0-1 scale")
    
    return df


def invert_negative_metrics(df: pd.DataFrame, negative_cols: list) -> pd.DataFrame:
    """Invert negative metrics so higher is always better"""
    for col in negative_cols:
        if col in df.columns:
            df[col] = 1 - df[col]
            print(f"  → Inverted: {col}")
    
    return df


def process_data():
    """Main processing pipeline"""
    Path(PROCESSED_DATA_DIR).mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("PROCESSING RAW DATA")
    print("="*60)
    
    # Load raw data
    df = load_raw_data()
    
    if df.empty:
        print("No data to process!")
        return
    
    # Identify columns
    col_mapping = identify_columns(df)
    print(f"\nIdentified columns: {col_mapping}")
    
    # Filter forwards
    df = filter_forwards(df, col_mapping)
    
    # Filter minimum minutes
    df = filter_minimum_minutes(df, col_mapping)
    
    # Normalize to per-90
    df = normalize_per_90(df, col_mapping)
    
    # Define feature columns for normalization
    feature_cols = [
        'goals_per90', 'assists_per90', 'xg_per90', 
        'npxg_per90', 'xag_per90'
    ]
    
    # Normalize features
    df = normalize_features(df, feature_cols)
    
    # Save processed data
    output_file = f"{PROCESSED_DATA_DIR}/forwards_processed.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved processed data: {output_file}")
    print(f"  Total forwards: {len(df)}")
    
    return df


if __name__ == "__main__":
    process_data()
