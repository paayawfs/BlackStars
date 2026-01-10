"""
Data Scraper for FBref using soccerdata library
Collects player statistics from multiple leagues
"""

import os
import time
import pandas as pd
import soccerdata as sd
from pathlib import Path

# Add parent directory to path for config import
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import LEAGUES, SEASONS, RAW_DATA_DIR, FORWARD_POSITIONS


def create_directories():
    """Create necessary data directories"""
    Path(RAW_DATA_DIR).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created directory: {RAW_DATA_DIR}")


def scrape_league_season(league: str, season: str) -> dict:
    """
    Scrape all relevant player stats for a single league and season
    
    Args:
        league: FBref league code (e.g., "ENG-Premier League")
        season: Season string (e.g., "2024-2025")
    
    Returns:
        Dictionary containing DataFrames for each stat type
    """
    print(f"\n{'='*60}")
    print(f"Scraping: {league} - {season}")
    print(f"{'='*60}")
    
    try:
        # Initialize FBref scraper for this league/season
        fbref = sd.FBref(leagues=[league], seasons=[season])
        
        stats = {}
        
        # Standard stats (goals, assists, minutes, etc.)
        print("  → Fetching standard stats...")
        try:
            stats['standard'] = fbref.read_player_season_stats(stat_type="standard")
            print(f"    ✓ Standard stats: {len(stats['standard'])} players")
        except Exception as e:
            print(f"    ✗ Standard stats failed: {e}")
            stats['standard'] = pd.DataFrame()
        
        time.sleep(4)  # Rate limiting
        
        # Shooting stats (shots, xG, npxG)
        print("  → Fetching shooting stats...")
        try:
            stats['shooting'] = fbref.read_player_season_stats(stat_type="shooting")
            print(f"    ✓ Shooting stats: {len(stats['shooting'])} players")
        except Exception as e:
            print(f"    ✗ Shooting stats failed: {e}")
            stats['shooting'] = pd.DataFrame()
        
        time.sleep(4)
        
        # Passing stats (key passes, xA)
        print("  → Fetching passing stats...")
        try:
            stats['passing'] = fbref.read_player_season_stats(stat_type="passing")
            print(f"    ✓ Passing stats: {len(stats['passing'])} players")
        except Exception as e:
            print(f"    ✗ Passing stats failed: {e}")
            stats['passing'] = pd.DataFrame()
        
        time.sleep(4)
        
        # Possession stats (progressive carries, touches)
        print("  → Fetching possession stats...")
        try:
            stats['possession'] = fbref.read_player_season_stats(stat_type="possession")
            print(f"    ✓ Possession stats: {len(stats['possession'])} players")
        except Exception as e:
            print(f"    ✗ Possession stats failed: {e}")
            stats['possession'] = pd.DataFrame()
        
        time.sleep(4)
        
        # Miscellaneous stats (aerials, fouls)
        print("  → Fetching misc stats...")
        try:
            stats['misc'] = fbref.read_player_season_stats(stat_type="misc")
            print(f"    ✓ Misc stats: {len(stats['misc'])} players")
        except Exception as e:
            print(f"    ✗ Misc stats failed: {e}")
            stats['misc'] = pd.DataFrame()
        
        time.sleep(4)
        
        # Goal and Shot Creation stats
        print("  → Fetching goal/shot creation stats...")
        try:
            stats['gca'] = fbref.read_player_season_stats(stat_type="gca")
            print(f"    ✓ GCA stats: {len(stats['gca'])} players")
        except Exception as e:
            print(f"    ✗ GCA stats failed: {e}")
            stats['gca'] = pd.DataFrame()
        
        return stats
        
    except Exception as e:
        print(f"  ✗ Failed to scrape {league} {season}: {e}")
        return {}


def filter_forwards(df: pd.DataFrame) -> pd.DataFrame:
    """Filter DataFrame to only include forwards/attackers"""
    if df.empty:
        return df
    
    # Check for position column (may have different names)
    pos_cols = ['Pos', 'pos', 'Position', 'position']
    pos_col = None
    
    for col in pos_cols:
        if col in df.columns:
            pos_col = col
            break
    
    if pos_col is None:
        # Try multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            for col in df.columns:
                if 'pos' in str(col).lower():
                    pos_col = col
                    break
    
    if pos_col is None:
        print("    ⚠ Could not find position column, returning all players")
        return df
    
    # Filter for forward positions
    mask = df[pos_col].astype(str).str.contains('|'.join(FORWARD_POSITIONS), case=False, na=False)
    filtered = df[mask]
    
    print(f"    → Filtered to {len(filtered)} forwards/attackers")
    return filtered


def save_stats(stats: dict, league: str, season: str):
    """Save scraped stats to CSV files"""
    league_clean = league.replace(" ", "_").replace("-", "_")
    season_clean = season.replace("-", "_")
    
    for stat_type, df in stats.items():
        if not df.empty:
            filename = f"{RAW_DATA_DIR}/{league_clean}_{season_clean}_{stat_type}.csv"
            df.to_csv(filename)
            print(f"  ✓ Saved: {filename}")


def scrape_all():
    """Main function to scrape all leagues and seasons"""
    create_directories()
    
    all_stats = []
    
    for season in SEASONS:
        for league in LEAGUES:
            stats = scrape_league_season(league, season)
            
            if stats:
                save_stats(stats, league, season)
                
                # Combine stats for this league/season
                if stats.get('standard') is not None and not stats['standard'].empty:
                    combined = stats['standard'].copy()
                    combined['league'] = league
                    combined['season'] = season
                    all_stats.append(combined)
            
            # Extra delay between leagues
            time.sleep(3)
    
    # Combine all data into master file
    if all_stats:
        master_df = pd.concat(all_stats, ignore_index=True)
        master_file = f"{RAW_DATA_DIR}/all_leagues_combined.csv"
        master_df.to_csv(master_file, index=False)
        print(f"\n{'='*60}")
        print(f"✓ Master file saved: {master_file}")
        print(f"  Total players: {len(master_df)}")
        print(f"{'='*60}")
    
    print("\n✓ Scraping complete!")


if __name__ == "__main__":
    scrape_all()
