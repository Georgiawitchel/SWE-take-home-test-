# Full-Stack SWE Coding Challenge: Virtual Patient Data Platform

## Overview

Welcome to the Virtual Patient Data Platform coding challenge! This assessment evaluates your ability to design and implement a full-stack application that handles complex biomedical data synchronization and visualization.

**Time Estimate:** 4-6 hours  
**Submission Deadline:** [INSERT DEADLINE]

---

## The Challenge

You are building a **Virtual Patient Application** for a research team that needs to analyze multi-modal biomedical data from patient monitoring devices. The challenge: each data stream (heart rate, movement, blood oxygen, etc.) comes from different sensors with **different sampling rates**, **timestamp formats**, and **data gaps**.

Your task is to build an application that:
1. Allows researchers to upload patient data files
2. Intelligently synchronizes misaligned time-series data
3. Provides an interactive interface to explore and analyze the synchronized data

---

## Dataset

You are provided with data for **3 patients**. Each patient has **5 data streams**:

| Data Type | Description | Typical Sampling Rate |
|-----------|-------------|----------------------|
| `heart_rate` | BPM readings from chest monitor | ~1 sample/sec |
| `movement` | Accelerometer data (x, y, z axes) | ~10 samples/sec |
| `blood_oxygen` | SpO2 percentage | ~0.5 samples/sec |
| `skin_temperature` | Temperature in Celsius | ~0.1 samples/sec |
| `load` | Physical exertion score (0-100) | ~0.2 samples/sec |

### Data Challenges (Intentional)

The provided data has **realistic imperfections** you must handle:

- ⏱️ **Timestamp misalignment**: Sensors started at different times
- 🕳️ **Data gaps**: Missing readings during sensor disconnections
- 📊 **Different sampling rates**: Heart rate updates faster than temperature
- 🔢 **Format variations**: Some files use Unix timestamps, others use ISO strings
- 📈 **Noise and outliers**: Some readings are clearly erroneous

---

## Requirements

### Backend (Node.js/Python/Go - your choice)

1. **Data Ingestion API**
   - Endpoint to upload CSV/JSON data files
   - Parse and validate incoming data
   - Store data efficiently (you may use any database or in-memory storage)

2. **Data Synchronization Engine**
   - Implement an algorithm to align time-series data with different timestamps
   - Handle gaps intelligently (interpolation, forward-fill, or flagging)
   - Support configurable sync strategies

3. **Query API**
   - Retrieve synchronized data for a patient
   - Support time-range queries
   - Return data in a format optimized for visualization

### Frontend (React)

1. **Data Upload Interface**
   - Upload multiple files per patient
   - Show upload progress and validation results
   - Display data quality indicators (gaps, outliers detected)

2. **Synchronization Controls**
   - Let users choose sync strategy (nearest neighbor, interpolation, etc.)
   - Preview how data will align before committing
   - Show a timeline of data coverage per stream

3. **Data Visualization & Interaction**
   - Display synchronized multi-stream data on a shared timeline
   - Interactive zoom/pan on time axis
   - Hover to see exact values across all streams at a point in time
   - Highlight data gaps and interpolated regions
   - Basic statistics panel (min, max, avg, data completeness %)

### Documentation

1. **README** for your solution explaining:
   - Architecture decisions and trade-offs
   - How to run the application
   - Your synchronization algorithm approach

2. **API Documentation** (OpenAPI/Swagger preferred, or clear markdown)

3. **Code Comments** for complex logic

---

## Evaluation Criteria

| Category | Weight | What We're Looking For |
|----------|--------|----------------------|
| **Data Sync Algorithm** | 25% | Correctness, handling edge cases, efficiency |
| **Backend Design** | 20% | Clean architecture, API design, error handling |
| **Frontend UX** | 20% | Intuitive interface, responsive design, accessibility |
| **Code Quality** | 15% | Readability, organization, TypeScript/typing usage |
| **Documentation** | 10% | Clear explanations, runnable instructions |
| **Bonus Features** | 10% | Creative solutions, performance optimizations |

### Bonus Points

- Export synchronized data to CSV/JSON
- Anomaly detection highlighting
- Real-time data streaming simulation
- Unit/integration tests
- Docker containerization
- Performance benchmarks with larger datasets

---

## Getting Started

### 1. Clone/Download This Repository

The `data/` folder contains all patient data files.

### 2. Explore the Data

```bash
data/
├── patient_001/
│   ├── heart_rate.csv
│   ├── movement.json
│   ├── blood_oxygen.csv
│   ├── skin_temperature.csv
│   └── load.json
├── patient_002/
│   └── ... (same structure)
├── patient_003/
│   └── ... (same structure)
└── schema.md          # Data format documentation
```

### 3. Build Your Solution

Create your application in a new folder (e.g., `solution/`).

### 4. Submit

Provide:
- Your complete source code
- Instructions to run locally
- A brief video walkthrough (optional but encouraged, 3-5 min)

---

## Technical Notes

### Recommended Tech Stack (not required)

- **Frontend:** React + TypeScript, Chart.js/Recharts/D3 for visualization
- **Backend:** Node.js with Express, or Python with FastAPI
- **Database:** PostgreSQL, SQLite, or even in-memory for this scale

### Data Volume

Each patient has approximately:
- 10,000 heart rate readings
- 100,000 movement readings
- 5,000 blood oxygen readings
- 1,000 temperature readings
- 2,000 load readings

This is intentionally large enough to require thoughtful data handling.

---

## Questions?

If you have clarifying questions about the requirements, please email [INSERT CONTACT].

**Good luck! We're excited to see your solution.** 🚀

