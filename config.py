"""
Configuration for Football Player Analytics Pipeline
"""

# Leagues to scrape from FBref
LEAGUES = [
    "ENG-Premier League",
    "ESP-La Liga", 
    "ITA-Serie A",
    "GER-Bundesliga",
    "FRA-Ligue 1",
    "ENG-Championship",
    "USA-MLS",
    "NED-Eredivisie"
]

# Seasons to scrape
SEASONS = ["2024-2025", "2025-2026"]

# Ghana Black Stars Forwards (as specified by user)
GHANA_FORWARDS = [
    "Mohammed Kudus",
    "Antoine Semenyo",
    "Jordan Ayew",
    "Ernest Nuamah",
    "Osman Bukari",
    "Fatawu Issahaku",
    "Kamaldeen Sulemana",
    "Ibrahim Osman",
    "Brandon Thomas-Asante",
    "Iñaki Williams",
    "Joseph Paintsil",
    "Jerry Afriyie",
    "Christopher Bonsu Baah"
]

# Alternative name mappings (FBref may use different spellings)
NAME_MAPPINGS = {
    "Mohammed Kudus": ["Kudus", "M. Kudus", "Mohammed Kudus"],
    "Antoine Semenyo": ["Semenyo", "A. Semenyo"],
    "Jordan Ayew": ["J. Ayew", "Jordan Ayew"],
    "Ernest Nuamah": ["Nuamah", "E. Nuamah"],
    "Osman Bukari": ["Bukari", "O. Bukari"],
    "Fatawu Issahaku": ["Fatawu", "Abdul Fatawu Issahaku", "A. Fatawu"],
    "Kamaldeen Sulemana": ["Kamaldeen", "K. Sulemana"],
    "Ibrahim Osman": ["I. Osman", "Ibrahim Osman"],
    "Brandon Thomas-Asante": ["Thomas-Asante", "B. Thomas-Asante"],
    "Iñaki Williams": ["Inaki Williams", "I. Williams", "Iñaki Williams"],
    "Joseph Paintsil": ["Paintsil", "J. Paintsil"],
    "Jerry Afriyie": ["Afriyie", "J. Afriyie"],
    "Christopher Bonsu Baah": ["C. Bonsu Baah", "Bonsu Baah"]
}

# Position filters for forwards/attackers
FORWARD_POSITIONS = ["FW", "MF,FW", "FW,MF", "LW", "RW", "ST", "CF", "AM"]

# Metrics to extract
METRICS = {
    "finishing": {
        "goals": "Gls",
        "npxg": "npxG", 
        "shots": "Sh",
        "shots_on_target": "SoT"
    },
    "creativity": {
        "xag": "xAG",
        "key_passes": "KP",
        "shot_creating_actions": "SCA",
        "goal_creating_actions": "GCA"
    },
    "progression": {
        "progressive_carries": "PrgC",
        "progressive_passes_received": "PrgR",
        "progressive_passes": "PrgP"
    },
    "retention": {
        "dispossessed": "Dis",  # Invert
        "miscontrols": "Mis"   # Invert
    },
    "physicality": {
        "aerials_won": "AerWon",
        "aerials_won_pct": "AerWon%"
    }
}

# Output directories
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"
OUTPUT_DIR = "outputs"

# Clustering configuration
MIN_MINUTES_PLAYED = 450  # Minimum 5 full games
N_CLUSTERS_RANGE = range(4, 10)  # Test 4-9 clusters
