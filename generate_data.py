#!/usr/bin/env python3
"""
Generate realistic patient biomedical data with PRONOUNCED imperfections
for the Virtual Patient coding challenge.

Key challenges:
- Large gaps (5-20 minutes) in data streams
- Different sensors start at very different times
- Random micro-gaps and dropouts
- Timestamp drift in some sensors
- Completely missing data segments
"""

import json
import csv
import random
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Seed for reproducibility
random.seed(42)

# Base timestamp: March 15, 2024, 8:00 AM UTC
BASE_TIME = datetime(2024, 3, 15, 8, 0, 0, tzinfo=timezone.utc)

# Patient configurations with LARGE offset differences
PATIENT_CONFIGS = {
    "patient_001": {
        "hr_offset": timedelta(minutes=0),
        "movement_offset": timedelta(minutes=7, seconds=23),  # Started 7+ min late
        "spo2_offset": timedelta(minutes=3, seconds=45),
        "temp_offset": timedelta(minutes=-15),  # Started 15 min BEFORE
        "load_offset": timedelta(minutes=12, seconds=8),  # Started 12+ min late
        "duration_hours": 2.5,
        "activity_pattern": "morning_routine",
        # Custom gaps for this patient
        "hr_gaps": [(1200, 420), (4200, 180), (6300, 540)],  # (start_sec, duration_sec)
        "movement_gaps": [(800, 300), (2400, 600), (5100, 240)],
        "spo2_gaps": [(1800, 1200), (5400, 300)],  # 20 min gap!
        "temp_gaps": [(3000, 180)],
        "load_gaps": [(900, 480), (3600, 360)],
    },
    "patient_002": {
        "hr_offset": timedelta(minutes=0),
        "movement_offset": timedelta(minutes=15, seconds=42),  # Very late start
        "spo2_offset": timedelta(minutes=5, seconds=10),
        "temp_offset": timedelta(minutes=-8),
        "load_offset": timedelta(minutes=2, seconds=30),
        "duration_hours": 3.0,
        "activity_pattern": "exercise_session",
        "hr_gaps": [(2100, 600), (5400, 900), (8400, 300)],  # 15 min gap in middle!
        "movement_gaps": [(1500, 180), (4800, 720), (7200, 240)],  # 12 min gap
        "spo2_gaps": [(3000, 480), (6600, 600)],
        "temp_gaps": [(4200, 300), (7800, 180)],
        "load_gaps": [(1800, 240), (5400, 420)],
    },
    "patient_003": {
        "hr_offset": timedelta(minutes=0),
        "movement_offset": timedelta(minutes=4, seconds=15),
        "spo2_offset": timedelta(minutes=22, seconds=30),  # Started 22+ min late!
        "temp_offset": timedelta(minutes=-25),  # Started 25 min before
        "load_offset": timedelta(minutes=8, seconds=45),
        "duration_hours": 2.0,
        "activity_pattern": "resting",
        "hr_gaps": [(1500, 300), (3600, 480)],
        "movement_gaps": [(900, 420), (2700, 180), (4500, 360)],
        "spo2_gaps": [(600, 540)],  # Early 9-min gap
        "temp_gaps": [(1800, 240), (4200, 180)],
        "load_gaps": [(2100, 300), (4800, 240)],
    }
}

def add_noise(value, noise_level=0.02):
    """Add gaussian noise to a value."""
    return value * (1 + random.gauss(0, noise_level))

def simulate_heart_rate(t_seconds, pattern):
    """Simulate realistic heart rate based on activity pattern."""
    base_hr = 70
    
    if pattern == "morning_routine":
        phase = (t_seconds % 3600) / 3600
        activity_component = 20 * math.sin(phase * math.pi * 2)
        base_hr = 65 + activity_component
    elif pattern == "exercise_session":
        normalized_t = t_seconds / (3 * 3600)
        if normalized_t < 0.3:
            base_hr = 70 + normalized_t * 100
        elif normalized_t < 0.7:
            base_hr = 130 + 20 * math.sin(normalized_t * 20)
        else:
            base_hr = 130 - (normalized_t - 0.7) * 200
    else:
        base_hr = 60 + 5 * math.sin(t_seconds / 600)
    
    return max(45, min(185, int(add_noise(base_hr, 0.03))))

def simulate_movement(t_seconds, pattern):
    """Simulate accelerometer data."""
    gravity = 9.81
    
    if pattern == "exercise_session":
        normalized_t = t_seconds / (3 * 3600)
        if 0.3 < normalized_t < 0.7:
            x = add_noise(random.uniform(-2, 2), 0.5)
            y = add_noise(-gravity + random.uniform(-1, 1), 0.1)
            z = add_noise(random.uniform(-2, 2), 0.5)
        else:
            x = add_noise(random.uniform(-0.2, 0.2), 0.3)
            y = add_noise(-gravity, 0.01)
            z = add_noise(random.uniform(-0.2, 0.2), 0.3)
    elif pattern == "morning_routine":
        if random.random() < 0.1:
            x = add_noise(random.uniform(-1, 1), 0.3)
            z = add_noise(random.uniform(-1, 1), 0.3)
        else:
            x = add_noise(0, 0.1)
            z = add_noise(0, 0.1)
        y = add_noise(-gravity, 0.01)
    else:
        x = add_noise(0, 0.05)
        y = add_noise(-gravity, 0.005)
        z = add_noise(0, 0.05)
    
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    return round(x, 3), round(y, 3), round(z, 3), round(magnitude, 3)

def simulate_spo2(t_seconds, pattern):
    """Simulate blood oxygen percentage."""
    base_spo2 = 98
    
    if pattern == "exercise_session":
        normalized_t = t_seconds / (3 * 3600)
        if 0.3 < normalized_t < 0.7:
            base_spo2 = 96 + random.uniform(-1, 1)
        else:
            base_spo2 = 98 + random.uniform(-0.5, 0.5)
    else:
        base_spo2 = 98 + random.uniform(-1, 1)
    
    return round(max(90, min(100, add_noise(base_spo2, 0.01))), 1)

def simulate_temperature(t_seconds, pattern):
    """Simulate skin temperature."""
    base_temp = 36.5
    
    if pattern == "exercise_session":
        normalized_t = t_seconds / (3 * 3600)
        if normalized_t > 0.3:
            base_temp = 36.5 + min(1.5, (normalized_t - 0.3) * 3)
    
    return round(add_noise(base_temp, 0.005), 2)

def simulate_load(t_seconds, hr, pattern):
    """Simulate physical load score."""
    if pattern == "exercise_session":
        normalized_t = t_seconds / (3 * 3600)
        if 0.3 < normalized_t < 0.7:
            return min(100, max(0, int(50 + (hr - 100) * 0.5 + random.randint(-5, 5))))
        else:
            return max(0, int(20 + random.randint(-5, 5)))
    elif pattern == "morning_routine":
        return max(0, min(100, int(25 + (hr - 70) * 0.3 + random.randint(-3, 3))))
    else:
        return max(0, int(10 + random.randint(-3, 3)))

def is_in_gap(t_seconds, gaps):
    """Check if current time falls within any gap period."""
    for gap_start, gap_duration in gaps:
        if gap_start <= t_seconds < gap_start + gap_duration:
            return True
    return False

def should_have_micro_dropout(probability=0.008):
    """Random micro-dropouts (brief signal loss)."""
    return random.random() < probability

def generate_heart_rate_data(patient_id, config):
    """Generate heart rate CSV data with gaps."""
    start_time = BASE_TIME + config["hr_offset"]
    duration = int(config["duration_hours"] * 3600)
    gaps = config["hr_gaps"]
    
    data = []
    t = 0
    # Simulate slight clock drift (sensor clock runs slightly fast/slow)
    drift_rate = random.uniform(-0.0001, 0.0001)  # up to 0.01% drift
    
    while t < duration:
        if not is_in_gap(t, gaps) and not should_have_micro_dropout(0.005):
            actual_t = t * (1 + drift_rate)  # Apply clock drift
            timestamp = start_time + timedelta(seconds=actual_t)
            hr = simulate_heart_rate(t, config["activity_pattern"])
            
            # Occasional sensor errors (more frequent than before)
            if random.random() < 0.008:
                hr = -1
                confidence = 0.0
            elif random.random() < 0.03:
                confidence = round(random.uniform(0.2, 0.5), 2)
            else:
                confidence = round(random.uniform(0.85, 0.99), 2)
            
            data.append({
                "timestamp": timestamp.isoformat(),
                "bpm": hr,
                "confidence": confidence
            })
        
        # Variable sampling rate (jitter)
        t += random.uniform(0.85, 1.15)
    
    return data

def generate_movement_data(patient_id, config):
    """Generate movement JSON data with gaps."""
    start_time = BASE_TIME + config["movement_offset"]
    duration = int(config["duration_hours"] * 3600)
    gaps = config["movement_gaps"]
    
    data = []
    t = 0
    
    while t < duration:
        if not is_in_gap(t, gaps) and not should_have_micro_dropout(0.003):
            timestamp_ms = int((start_time + timedelta(seconds=t)).timestamp() * 1000)
            x, y, z, mag = simulate_movement(t, config["activity_pattern"])
            
            record = {
                "ts": timestamp_ms,
                "x": x,
                "y": y,
                "z": z,
                "magnitude": mag
            }
            
            # Occasional null/corrupt values (more frequent)
            if random.random() < 0.004:
                record["x"] = None
                record["magnitude"] = None
            elif random.random() < 0.002:
                # Completely corrupt reading
                record["x"] = 999.99
                record["y"] = 999.99
                record["z"] = 999.99
                record["magnitude"] = 999.99
            
            data.append(record)
        
        # ~10 samples per second with jitter
        t += random.uniform(0.08, 0.12)
    
    return data

def generate_blood_oxygen_data(patient_id, config):
    """Generate blood oxygen CSV data with gaps."""
    start_time = BASE_TIME + config["spo2_offset"]
    duration = int(config["duration_hours"] * 3600)
    gaps = config["spo2_gaps"]
    
    data = []
    t = 0
    
    while t < duration:
        if not is_in_gap(t, gaps) and not should_have_micro_dropout(0.01):
            # Unix timestamp in SECONDS (intentionally different!)
            timestamp_sec = int((start_time + timedelta(seconds=t)).timestamp())
            spo2 = simulate_spo2(t, config["activity_pattern"])
            
            if spo2 >= 97:
                quality = "good"
            elif spo2 >= 94:
                quality = "fair"
            else:
                quality = "poor"
            
            # Occasional erroneous readings
            if random.random() < 0.005:
                spo2 = round(random.uniform(65, 84), 1)  # Clearly wrong
                quality = "poor"
            elif random.random() < 0.003:
                spo2 = round(random.uniform(101, 110), 1)  # Impossible high
                quality = "poor"
            
            data.append({
                "time": timestamp_sec,
                "spo2": spo2,
                "pulse_quality": quality
            })
        
        # ~0.5 samples per second with irregular intervals
        t += random.uniform(1.5, 2.5)
    
    return data

def generate_temperature_data(patient_id, config):
    """Generate skin temperature CSV data with gaps."""
    start_time = BASE_TIME + config["temp_offset"]
    # Temperature sensor runs longer since it started earlier
    extra_duration = abs(config["temp_offset"].total_seconds()) + 600
    duration = int(config["duration_hours"] * 3600 + extra_duration)
    gaps = config["temp_gaps"]
    
    # Use different timezone (intentional challenge!)
    tz_offset = timezone(timedelta(hours=-5))  # EST
    
    data = []
    t = 0
    ambient_temp = round(random.uniform(20, 24), 1)
    
    while t < duration:
        if not is_in_gap(t, gaps) and not should_have_micro_dropout(0.015):
            timestamp = (start_time + timedelta(seconds=t)).astimezone(tz_offset)
            temp = simulate_temperature(t, config["activity_pattern"])
            
            # Temperature spikes from contact issues
            if random.random() < 0.015:
                temp = round(temp + random.uniform(3, 8), 2)  # Big spike
            elif random.random() < 0.01:
                temp = round(temp - random.uniform(2, 5), 2)  # Sensor lift-off
            
            # Ambient temp slowly drifts
            ambient_temp += random.uniform(-0.02, 0.02)
            ambient_temp = max(18, min(28, ambient_temp))
            
            data.append({
                "recorded_at": timestamp.isoformat(),
                "temp_celsius": temp,
                "ambient_temp": round(ambient_temp, 1)
            })
        
        # Very slow sampling (~0.1 samples/sec) with high variance
        t += random.uniform(8, 14)
    
    return data

def generate_load_data(patient_id, config):
    """Generate physical load JSON data with gaps."""
    start_time = BASE_TIME + config["load_offset"]
    duration = int(config["duration_hours"] * 3600)
    gaps = config["load_gaps"]
    
    data = []
    t = 0
    
    while t < duration:
        if not is_in_gap(t, gaps) and not should_have_micro_dropout(0.012):
            hr = simulate_heart_rate(t, config["activity_pattern"])
            load = simulate_load(t, hr, config["activity_pattern"])
            
            # Variable timestamp precision (intentional inconsistency)
            timestamp = start_time + timedelta(seconds=t)
            rand = random.random()
            if rand < 0.3:
                ts_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")  # No ms
            elif rand < 0.6:
                ts_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.") + f"{random.randint(0, 999):03d}Z"  # With ms
            else:
                # Sometimes use a completely different format!
                ts_str = timestamp.strftime("%Y/%m/%d %H:%M:%S")  # Slash format
            
            if load < 20:
                activity = "rest"
            elif load < 50:
                activity = "walk"
            else:
                activity = "exercise"
            
            # Error values
            if random.random() < 0.015:
                load = -1
                activity = "unknown"
            
            data.append({
                "timestamp": ts_str,
                "load_score": load,
                "activity_type": activity,
                "hr_derived": random.random() < 0.7
            })
        
        # ~0.2 samples per second
        t += random.uniform(4, 6)
    
    return data

def save_csv(data, filepath, fieldnames):
    """Save data to CSV file."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def save_json(data, filepath):
    """Save data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=None)

def print_gap_summary(patient_id, config):
    """Print summary of gaps for reference."""
    print(f"\n  Gap Summary for {patient_id}:")
    print(f"    Heart Rate: {len(config['hr_gaps'])} gaps, total {sum(g[1] for g in config['hr_gaps'])//60} min")
    print(f"    Movement: {len(config['movement_gaps'])} gaps, total {sum(g[1] for g in config['movement_gaps'])//60} min")
    print(f"    SpO2: {len(config['spo2_gaps'])} gaps, total {sum(g[1] for g in config['spo2_gaps'])//60} min")
    print(f"    Temperature: {len(config['temp_gaps'])} gaps, total {sum(g[1] for g in config['temp_gaps'])//60} min")
    print(f"    Load: {len(config['load_gaps'])} gaps, total {sum(g[1] for g in config['load_gaps'])//60} min")

def print_offset_summary(patient_id, config):
    """Print summary of time offsets."""
    print(f"\n  Start Time Offsets (relative to heart rate):")
    print(f"    Heart Rate: T+0:00")
    print(f"    Movement: T+{int(config['movement_offset'].total_seconds()//60)}:{int(config['movement_offset'].total_seconds()%60):02d}")
    print(f"    SpO2: T+{int(config['spo2_offset'].total_seconds()//60)}:{int(config['spo2_offset'].total_seconds()%60):02d}")
    td = config['temp_offset']
    print(f"    Temperature: T{int(td.total_seconds()//60)}:{abs(int(td.total_seconds()%60)):02d}")
    print(f"    Load: T+{int(config['load_offset'].total_seconds()//60)}:{int(config['load_offset'].total_seconds()%60):02d}")

def main():
    base_path = Path(__file__).parent / "data"
    
    for patient_id, config in PATIENT_CONFIGS.items():
        print(f"\n{'='*60}")
        print(f"Generating data for {patient_id}...")
        print_offset_summary(patient_id, config)
        print_gap_summary(patient_id, config)
        
        patient_path = base_path / patient_id
        patient_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n  Generating files:")
        
        print(f"    - Heart rate...", end=" ")
        hr_data = generate_heart_rate_data(patient_id, config)
        save_csv(hr_data, patient_path / "heart_rate.csv", ["timestamp", "bpm", "confidence"])
        print(f"{len(hr_data)} records")
        
        print(f"    - Movement...", end=" ")
        movement_data = generate_movement_data(patient_id, config)
        save_json(movement_data, patient_path / "movement.json")
        print(f"{len(movement_data)} records")
        
        print(f"    - Blood oxygen...", end=" ")
        spo2_data = generate_blood_oxygen_data(patient_id, config)
        save_csv(spo2_data, patient_path / "blood_oxygen.csv", ["time", "spo2", "pulse_quality"])
        print(f"{len(spo2_data)} records")
        
        print(f"    - Skin temperature...", end=" ")
        temp_data = generate_temperature_data(patient_id, config)
        save_csv(temp_data, patient_path / "skin_temperature.csv", ["recorded_at", "temp_celsius", "ambient_temp"])
        print(f"{len(temp_data)} records")
        
        print(f"    - Physical load...", end=" ")
        load_data = generate_load_data(patient_id, config)
        save_json(load_data, patient_path / "load.json")
        print(f"{len(load_data)} records")
    
    print(f"\n{'='*60}")
    print("All patient data generated successfully!")
    print("\nKey challenges in the data:")
    print("  • Sensors start at VERY different times (up to 25 min apart)")
    print("  • Multiple gaps per stream (5-20 minutes each)")
    print("  • Different timestamp formats (Unix ms, Unix sec, ISO, slash format)")
    print("  • Different timezones (UTC vs EST)")
    print("  • Sensor errors (-1 values, nulls, impossible readings)")
    print("  • Clock drift in heart rate sensor")
    print("  • Micro-dropouts throughout")

if __name__ == "__main__":
    main()
