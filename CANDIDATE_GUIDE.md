# Candidate Quick-Start Guide

Wlecome to the mantis biotech SWE Coding challenge. As an employee at an early stage startup, you have a ton of creative freedom to come 
up with solutions to unique challenges. This test is less to see if you can write code (AI can do this) and more to see how you go about solving problems. 
As you complete this coding test think about teh following 

1. usability: The person who uses this prodcut is not a coding expert... the product should be easy and intuitive for them to use 
2. Dynamicness: If we cahnge around data types, adding or removing one... how much code factoring will be necessary 
3. Security: This platform will need to be HIPPA compliant. In this coding test we don't ask that you set up GCS or make it HIPPA 
compliant but add in notes regarding where you would require additional authentication and how you would handle these types of security risks. 

Your task: 

You're job is to create a react interface for a HIPPA compliant patient analysis and management software. This product is for a company that collects a huge amount of patent data and aligns it into a signular patient model. Companies can log in with a company email and immediately be logged into their organization, where 
they can create or update patients. Each patient has a series of data associated with them (It can be in a bunch of different forms). We want users to be 
able to easily upload or add any type of patient data, and we'll combine all of the data into a singular queryable patient model. 

Example data for each patient is located in data. You'll notice the data has a bunch of gaps... you'll need to figure out the best way to align this data 
given that it has many gaps, and display it back to the user in such a way that they can easily understand how all of this data contributed 
to a singular patient model. 

Create a react + electron frontend and a python backend that runs in docker. Document your work as you go 

You can work on this at whatever speed you'd like but don't spend more than 6 hours on this... I'd reccomend you spend 3. 

Submission: 
1. Send an email to georgia@mantisbiotech.com with your zipped codebase and instructions for running the application 
2. upload a video walkthrough to google drive and share the link for the wlakthrough 


## 📁 Repository Structure

```
├── README.md                 # Full challenge description & requirements
├── CANDIDATE_GUIDE.md        # You are here
├── data/
│   ├── patient_001/
│   │   ├── heart_rate.csv   # ~8,500 records, ISO timestamps
│   │   ├── movement.json    # ~87,000 records, Unix ms timestamps
│   │   ├── blood_oxygen.csv # ~4,000 records, Unix SECONDS (!)
│   │   ├── skin_temperature.csv # ~1,000 records, ISO with timezone
│   │   └── load.json        # ~1,700 records, mixed precision
│   ├── patient_002/         # Same structure, different offsets
│   └── patient_003/         # Same structure, different offsets
└── generate_data.py         # (For reference - how data was generated)
```

## ⚡ Quick Tips

###  Key Data Challenges to Handle

| Challenge | Where It Appears |
|-----------|-----------------|
| Unix ms vs seconds | `movement.json` (ms) vs `blood_oxygen.csv` (**seconds!**) |
| Different timezones | `skin_temperature.csv` uses **EST (-05:00)**, others use UTC |
| **Mixed timestamp formats** | `load.json` has 3 formats: ISO, ISO+ms, **slash format** |
| Sensor errors | `bpm: -1`, `null` values, `999.99` corrupt readings |
| **Large data gaps** | 5-30 min gaps throughout each stream |
| **Very different start times** | Sensors started **up to 25 min apart!** |
| Impossible values | SpO2 > 100%, temp spikes > 40°C |

### 3. Suggested Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Upload  │  │  Sync Config │  │   Timeline Viewer      │ │
│  │  Panel   │  │   Controls   │  │   (Chart.js/D3/etc)    │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Node/Python/Go)                  │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Upload  │  │  Sync Engine │  │   Query API            │ │
│  │  Service │  │  (core algo) │  │   (time ranges, etc)   │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Bonus Points Opportunities

- Dockerize the application
- Add unit tests for the sync algorithm
- Implement anomaly detection (highlight unusual values)
- Add data export (CSV/JSON)
- Performance optimize for smooth 100k+ point visualization



Looking forward to seeing what you create!  
Georgia. 

