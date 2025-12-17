# Data Schema Documentation

## Overview

This document describes the format of all patient data files. **⚠️ Warning:** The data intentionally has significant inconsistencies that candidates must handle.

---

## File Formats

### CSV Files
- Comma-separated values
- First row is header
- **Timestamps vary by file** - may be Unix milliseconds, Unix seconds, or ISO 8601

### JSON Files
- Array of objects
- Each object represents one reading
- Timestamps vary (Unix ms or ISO strings with variable precision)

---

## Data Stream Schemas

### Heart Rate (`heart_rate.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | ISO 8601 string | When reading was taken (UTC) |
| `bpm` | integer | Beats per minute (typically 40-200) |
| `confidence` | float | Sensor confidence score (0.0-1.0) |

**Example:**
```csv
timestamp,bpm,confidence
2024-03-15T08:00:00+00:00,72,0.95
2024-03-15T08:00:01.035340+00:00,73,0.97
```

**Known Issues:**
- `bpm: -1` indicates sensor error
- Confidence below 0.5 indicates unreliable reading
- **Multiple gaps** (5-10 min each) throughout recording
- Slight clock drift (~0.01%) over recording period

---

### Movement (`movement.json`)

| Field | Type | Description |
|-------|------|-------------|
| `ts` | integer | **Unix timestamp in MILLISECONDS** |
| `x` | float | X-axis acceleration (m/s²) |
| `y` | float | Y-axis acceleration (m/s²) |
| `z` | float | Z-axis acceleration (m/s²) |
| `magnitude` | float | Computed √(x² + y² + z²) |

**Example:**
```json
[
  {"ts": 1710489600000, "x": 0.02, "y": -9.81, "z": 0.15, "magnitude": 9.81},
  {"ts": 1710489600100, "x": 0.05, "y": -9.78, "z": 0.18, "magnitude": 9.78}
]
```

**Known Issues:**
- **Started 4-15 minutes AFTER** heart rate sensor depending on patient
- `null` values when sensor was bumped
- `999.99` values indicate corrupt readings (filter these out!)
- Multiple gaps throughout

---

### Blood Oxygen (`blood_oxygen.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `time` | integer | **Unix timestamp in SECONDS** (not ms!) |
| `spo2` | float | Blood oxygen percentage (typically 90-100%) |
| `pulse_quality` | string | "good", "fair", or "poor" |

**Example:**
```csv
time,spo2,pulse_quality
1710489600,98.5,good
1710489602,98.3,good
```

**⚠️ CRITICAL:** Uses Unix **SECONDS** not milliseconds unlike other streams!

**Known Issues:**
- **Large gaps** (up to 25 min) when patient removed sensor
- Values below 85% are likely erroneous
- Values above 100% are sensor errors (yes, they exist!)
- Started 3-22 minutes after heart rate depending on patient

---

### Skin Temperature (`skin_temperature.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `recorded_at` | ISO 8601 string | **Timestamp WITH TIMEZONE OFFSET** |
| `temp_celsius` | float | Temperature in Celsius |
| `ambient_temp` | float | Room temperature (for reference) |

**Example:**
```csv
recorded_at,temp_celsius,ambient_temp
2024-03-15T02:45:00-05:00,36.2,22.1
2024-03-15T02:45:10-05:00,36.3,22.1
```

**⚠️ CRITICAL:** Uses **EST timezone (-05:00)** while heart rate uses UTC!

**Known Issues:**
- **Started 8-25 minutes BEFORE** heart rate sensor (negative offset)
- Very slow sampling rate (~1 reading per 10 seconds)
- Temperature spikes (>40°C) indicate sensor contact issues
- Temperature drops (<34°C) indicate sensor lift-off

---

### Physical Load (`load.json`)

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | **MIXED FORMATS** (see below!) |
| `load_score` | integer | Exertion level 0-100 |
| `activity_type` | string | "rest", "walk", "exercise", "unknown" |
| `hr_derived` | boolean | Whether calculated from heart rate |

**⚠️ CRITICAL:** The `timestamp` field uses THREE DIFFERENT FORMATS:
1. ISO 8601 without milliseconds: `"2024-03-15T08:12:32Z"`
2. ISO 8601 with milliseconds: `"2024-03-15T08:12:13.927Z"`
3. **Slash format (no timezone!):** `"2024/03/15 08:12:17"`

**Example (mixed formats):**
```json
[
  {"timestamp": "2024-03-15T08:12:13.927Z", "load_score": 24, ...},
  {"timestamp": "2024/03/15 08:12:17", "load_score": 26, ...},
  {"timestamp": "2024-03-15T08:12:32Z", "load_score": 21, ...}
]
```

**Known Issues:**
- `load_score: -1` means "unable to calculate"
- Started 2-12 minutes after heart rate sensor
- Multiple gaps throughout

---

## Timestamp Alignment Challenge

The sensors were NOT synchronized at start. Here's the approximate offset for each patient:

| Patient | Heart Rate | Movement | SpO2 | Temperature | Load |
|---------|------------|----------|------|-------------|------|
| 001 | T+0:00 | **T+7:23** | T+3:45 | **T-15:00** | **T+12:08** |
| 002 | T+0:00 | **T+15:42** | T+5:10 | T-8:00 | T+2:30 |
| 003 | T+0:00 | T+4:15 | **T+22:30** | **T-25:00** | T+8:45 |

Where `T+0:00` is when heart rate monitoring began.

**⚠️ Note:** Some offsets are VERY large (up to 25 minutes)! Temperature sensors started BEFORE heart rate in all cases.

---

## Gap Summary

Each data stream has multiple gaps. Here's the total gap time per patient:

| Patient | Heart Rate | Movement | SpO2 | Temperature | Load |
|---------|------------|----------|------|-------------|------|
| 001 | ~19 min (3 gaps) | ~19 min (3 gaps) | **~25 min** (2 gaps) | ~3 min | ~14 min |
| 002 | **~30 min** (3 gaps) | ~19 min (3 gaps) | ~18 min | ~8 min | ~11 min |
| 003 | ~13 min (2 gaps) | ~16 min (3 gaps) | ~9 min | ~7 min | ~9 min |

---

## Data Quality Flags

When processing data, candidates MUST handle:

1. **Gaps**: Any period > 2x the expected sampling interval
2. **Outliers**: Values outside physiological ranges
   - Heart rate: < 40 or > 200 bpm
   - SpO2: < 85% or > 100%
   - Temperature: < 34°C or > 42°C
3. **Sensor Errors**: Values of -1, null, 999.99
4. **Low Confidence**: Heart rate readings with confidence < 0.5

---

## Expected Data Duration

Each patient's monitoring session is approximately **2-3 hours** of data (excluding gaps).

## File Sizes (Approximate)

| File | Size | Record Count |
|------|------|--------------|
| heart_rate.csv | ~300-400 KB | ~6,000-9,000 rows |
| movement.json | ~5-8 MB | ~60,000-100,000 records |
| blood_oxygen.csv | ~100-150 KB | ~3,000-5,000 rows |
| skin_temperature.csv | ~35-50 KB | ~800-1,000 rows |
| load.json | ~100-150 KB | ~1,300-2,000 records |

