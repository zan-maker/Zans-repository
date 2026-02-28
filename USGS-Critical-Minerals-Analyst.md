# USGS Critical Minerals Analyst

## Overview

AI-powered mining data intelligence system that extracts critical mineral mining data from USGS sources daily, analyzes with Mistral AI, and identifies contact information for mine outreach.

## Features

- **Daily Automation:** Cron job runs at 9:00 AM EST
- **Mistral AI Integration:** Document analysis of geological surveys
- **USGS Data Sources:** USMIN Mineral Deposit Database, MRDATA API, National Inventories
- **Intelligent Scoring:** Prospect evaluation algorithm
- **Contact Identification:** Mine owner outreach system

## Data Coverage

- **Geographic Focus:** US, Canada, Latin America
- **Commodities:** Gold (1M+ oz), Silver, Copper, Rare Earths
- **Excluded:** Platinum Group Metals, Nickel, Zinc, Aluminum, Lithium, Cobalt
- **Sources:** USGS geological surveys, mine databases, government reports

## Technical Stack

- **AI Model:** Mistral AI (Document AI for API search)
- **Automation:** OpenClaw cron jobs
- **Integration:** GitHub, Google Cloud (media generation)
- **Data:** USGS APIs, MRDATA, USMIN Database

## Setup

1. Configure Mistral AI API key
2. Set up daily cron job
3. Configure GitHub integration
4. Add Google Cloud API for media

## Output

- Daily reports with prospect lists
- Contact information for mine owners
- Media files (screenshots, videos)
- GitHub repository updates
