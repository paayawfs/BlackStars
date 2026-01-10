# Football Player Analytics Pipeline

A comprehensive data science project for analyzing football forwards using FBref statistics, unsupervised machine learning (K-Means clustering), and tactical recommendations for the Ghana Black Stars.

## 🎯 Project Overview

This project:
1. **Collects** player statistics from 8 major leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Championship, MLS, Eredivisie)
2. **Clusters** ~2,000 forwards into player archetypes using K-Means
3. **Analyzes** Ghana national team players in global context
4. **Recommends** optimal lineups based on data insights

## 📁 Project Structure

```
FBref/
├── notebooks/
│   ├── 01_data_collection.ipynb    # Scrape FBref data
│   ├── 02_data_processing.ipynb    # Clean & normalize data
│   ├── 03_clustering.ipynb         # K-Means clustering
│   └── 04_ghana_analysis.ipynb     # Ghana deep dive & recommendations
├── data/
│   ├── raw/                        # Raw scraped data
│   └── processed/                  # Cleaned, normalized data
├── outputs/
│   ├── cluster_scatter.png         # All forwards visualization
│   ├── ghana_global_scatter.png    # Ghana players highlighted
│   ├── radar_*.png                 # Player comparison charts
│   └── clustering_model.pkl        # Saved ML model
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Notebooks

Run the notebooks in order:

1. **01_data_collection.ipynb** - Scrapes FBref (takes 30-60 min)
2. **02_data_processing.ipynb** - Cleans and normalizes data
3. **03_clustering.ipynb** - Runs K-Means clustering
4. **04_ghana_analysis.ipynb** - Ghana analysis and visualizations

## 📊 What is `soccerdata`?

The `soccerdata` library is the backbone of our data collection. It:

- **Scrapes FBref** without you writing complex HTML parsers
- **Handles rate limiting** (FBref blocks fast scrapers)
- **Caches data** so you don't re-scrape the same pages
- **Returns Pandas DataFrames** ready for analysis

Example usage:
```python
import soccerdata as sd

# Get Premier League shooting stats
fbref = sd.FBref(leagues=["ENG-Premier League"], seasons=["2024-2025"])
shooting = fbref.read_player_season_stats(stat_type="shooting")
```

## 🇬🇭 Ghana Players Analyzed

1. Mohammed Kudus
2. Antoine Semenyo
3. Jordan Ayew
4. Ernest Nuamah
5. Osman Bukari
6. Fatawu Issahaku
7. Kamaldeen Sulemana
8. Ibrahim Osman
9. Brandon Thomas-Asante
10. Iñaki Williams
11. Joseph Paintsil
12. Jerry Afriyie
13. Christopher Bonsu Baah

## 📈 Outputs

### Scatter Plot
A 2D visualization showing where Ghana players sit among ~2,000 global forwards.

### Radar Charts
Direct comparisons between players (e.g., Fatawu vs Nuamah) showing percentile rankings.

### Cluster Profiles
Automatically discovered player archetypes like:
- 🦊 Fox in the Box (Poacher)
- 🎨 Creative Playmaker
- ⚡ Complete Forward
- 🔄 Balanced Forward

### Tactical Recommendations
Data-backed lineup suggestions for:
- **Dominant lineup** (vs weaker teams)
- **Counter-attack lineup** (vs stronger teams)
- **Plan B** impact substitutes

## ⚠️ Important Notes

1. **Rate Limiting**: FBref requires 3-6 second delays between requests. Full scraping takes 30-60 minutes.

2. **Data Freshness**: Run `01_data_collection.ipynb` to get the latest stats.

3. **Missing Players**: Some players may not appear if they haven't played enough minutes (minimum 450 minutes).

## 📝 License

This project is for educational/analytical purposes only. FBref data is subject to their terms of service.
"# BlackStars" 
