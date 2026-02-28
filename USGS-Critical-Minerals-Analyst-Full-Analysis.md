# USGS Critical Minerals Analyst — Full Technical Analysis

## System Architecture

### 1. Data Extraction Layer

- **USMIN Database:** Comprehensive mineral deposit information
- **MRDATA API:** Real-time geological data access
- **National Inventories:** Mine waste and resource data
- **Critical Minerals:** Focus on lithium, cobalt, rare earth elements

### 2. AI Analysis Layer

- **Mistral AI Integration:** Document analysis of geological surveys
- **Natural Language Processing:** Extract insights from PDF reports
- **Data Validation:** Cross-reference multiple sources
- **Pattern Recognition:** Identify promising prospects

### 3. Automation Layer

- **Daily Cron Job:** 9:00 AM EST execution
- **Error Handling:** Automatic retry and notification
- **Data Storage:** Structured output in JSON/CSV formats
- **Media Generation:** Screenshots and video recording

### 4. Output Layer

- **Reports:** Daily analysis with prospect lists
- **Contacts:** Mine owner information for outreach
- **Media:** Dashboard screenshots and video demos
- **GitHub:** Version-controlled repository updates

## Technical Specifications

### API Configuration
