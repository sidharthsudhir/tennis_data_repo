# ATP Tennis Matches 2024 Analysis

Interactive dashboard analyzing ATP tennis matches from 2024 using Python and Preswald.

## Overview

This project analyzes 3,000+ ATP tennis matches from 2024, providing insights into tournament results, player performance, and tennis-specific metrics. Built for tennis fans and data enthusiasts.

## Features

- **Tournament Results**: Finals, champions, and player win counts
- **Match Highlights**: Longest matches, most aces, biggest upsets  
- **Interactive Filtering**: Age-based analysis with dynamic controls
- **Tennis Analytics**: Serve performance, break points, surface analysis
- **Player Data**: Head-to-head matchups, rankings, nationalities

## Dataset

Source: `data/atpmatches2024.csv`
- 3,000+ matches from Grand Slams, Masters, ATP 250/500 events
- Player stats, match scores, serve data, rankings, tournament info

## Structure
```
my_assessment_app/
├── data/
│   └── atpmatches2024.csv      # ATP matches dataset
├── images/
│   ├── favicon.ico             # App favicon
│   └── logo.png               # App logo
├── hello.py                   # Main analysis script
├── preswald.toml             # Configuration file
├── secrets.toml              # Secrets configuration
├── preswald_export/          # Static site export
│   ├── index.html           # Exported HTML app
│   ├── project_fs.json      # Project files
│   └── assets/              # CSS/JS assets
└── README.md                # This file
```
