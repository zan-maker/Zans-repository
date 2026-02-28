# USGS Critical Minerals Analyst — Enhanced Report

## Executive Summary

The USGS Critical Minerals Analyst is an AI-powered system that automates daily extraction of critical mineral mining data from USGS sources, analyzes geological information using Mistral AI, and identifies contact information for mine outreach.

## Key Features

- **Daily Automation:** Cron job runs at 9:00 AM EST
- **Mistral AI Integration:** Document analysis of USGS geological surveys
- **USGS Data Pipeline:** USMIN, MRDATA, National Inventories
- **Intelligent Scoring:** Prospect evaluation algorithm
- **Contact System:** Mine owner identification & outreach

## Data Coverage

- **Geography:** US, Canada, Latin America only
- **Commodities:** Gold (1M+ oz), Silver, Copper, Rare Earths
- **Sources:** USGS APIs, geological surveys, mine databases
- **Output:** Daily reports, prospect lists, contact info

## Technical Implementation

- **AI Model:** Mistral AI (Document AI for API search)
- **Automation:** OpenClaw cron jobs
- **Integration:** GitHub, Google Cloud (media)
- **Data:** USGS APIs, MRDATA, USMIN Database

## Dashboard Demo

![USGS Critical Minerals Dashboard](media/dashboard-demo.jpg)

**Dashboard Features:**

1. **Data Extraction Panel** — Real-time processing of USMIN/MRDATA APIs
2. **AI Document Analysis** — Mistral AI analyzing geological survey PDFs
3. **Intelligent Prospect Scoring** — Interactive US map with prospect locations

**Video Demonstration:** The dashboard includes a video showing the complete workflow from data extraction to prospect scoring.
