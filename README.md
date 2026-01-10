# ⚽ Football Player Analytics Pipeline

A data science project for analyzing football forwards using FBref statistics and K-Means clustering, with a focus on Ghana Black Stars squad analysis.

## 🎯 Overview

This project:
1. **Scrapes** player statistics from 7 major leagues via Selenium
2. **Processes** 50+ per-90 metrics across shooting, passing, possession, defense, and more
3. **Clusters** ~700 unique forwards into player archetypes using K-Means
4. **Analyzes** Ghana national team players in global context

## 📁 Project Structure

```
FBref/
├── notebooks/
│   ├── 01_data_collection.ipynb    # Basic FBref scraping
│   ├── 01b_scrape_all_stats.ipynb  # Full stats (shooting, passing, etc.)
│   ├── 02_data_processing.ipynb    # Clean, merge & normalize data
│   ├── 03_clustering.ipynb         # K-Means clustering
│   └── 04_ghana_analysis.ipynb     # Ghana deep dive
├── src/
│   ├── scraper.py                  # Selenium scraping functions
│   ├── processor.py                # Data processing pipeline
│   └── clustering.py               # Clustering utilities
├── scripts/
│   └── run_ghana_analysis.py       # Standalone Ghana analysis script
├── data/
│   ├── raw/                        # Raw scraped CSVs (gitignored)
│   └── processed/                  # Final processed dataset
├── outputs/                        # Generated visualizations & models
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
└── .gitignore
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Pipeline

**Option A: Use existing processed data**
- Skip to notebook `03_clustering.ipynb` (processed data included in repo)

**Option B: Scrape fresh data**
Run notebooks in order:
1. `01b_scrape_all_stats.ipynb` - Scrapes all stat types (~45 min)
2. `02_data_processing.ipynb` - Merges and normalizes
3. `03_clustering.ipynb` - Runs K-Means clustering
4. `04_ghana_analysis.ipynb` - Ghana analysis

## 📊 Data Sources

Data scraped from [FBref](https://fbref.com) covering:
- **Leagues**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, Championship, Eredivisie
- **Stat Types**: Standard, Shooting, Passing, Possession, Defense, Misc, GCA

## 🇬🇭 Ghana Players Tracked

| Player | Club | League |
|--------|------|--------|
| Mohammed Kudus | West Ham | Premier League |
| Antoine Semenyo | Bournemouth | Premier League |
| Jordan Ayew | Crystal Palace | Premier League |
| Fatawu Issahaku | Leicester City | Championship |
| Iñaki Williams | Athletic Bilbao | La Liga |
| Kamaldeen Sulemana | Southampton | Championship |
| Ernest Nuamah | Lyon | Ligue 1 |
| + 6 more | | |

## 📈 Outputs

- **Cluster profiles** with statistical descriptions (no arbitrary names)
- **Radar charts** comparing player percentile rankings
- **Scatter plots** showing Ghana players vs global forwards
- **Tactical recommendations** for lineup selection

## ⚙️ Configuration

Edit `config.py` to customize:
- `MIN_MINUTES_PLAYED`: Minimum playing time filter (default: 450)
- `FORWARD_POSITIONS`: Position codes to include
- `CLUSTERING_FEATURES`: Metrics used for clustering

## ⚠️ Notes

- **Rate limiting**: FBref requires 6-10 second delays between requests
- **Scraping time**: Full scrape takes ~45 minutes
- **Minimum minutes**: Players with <450 minutes are excluded

## 📝 License

For educational/analytical purposes only. FBref data subject to their terms of service.
