# Data Handling Documentation

## Overview

This document describes the data validation, cleaning, and missing data handling strategies used in the CityBike application.

## Data Sources

| File | Description |
|------|-------------|
| `data/trips.csv` | Trip records with user, bike, station, and timing information |
| `data/stations.csv` | Station metadata including location and capacity |
| `data/maintenance.csv` | Bike maintenance records |

---

## Missing Data Handling Strategy

### Rationale: Drop vs Fill

We chose to **drop rows with missing values** rather than impute (fill) them for the following reasons:

| Approach | When to Use | Why We Chose Drop |
|----------|-------------|-------------------|
| **Drop** | Critical fields where imputation would introduce bias | Trip IDs, station IDs, and timestamps are identifiers — filling them with synthetic values would create false records |
| **Fill (Mean/Median)** | Continuous numeric data with random missingness | `duration_minutes` and `distance_km` could theoretically be imputed, but missing values often indicate incomplete/cancelled trips rather than random sensor failures |
| **Fill (Mode)** | Categorical data with small % missing | Our categorical fields (`user_type`, `bike_type`) have very low missing rates; imputing would add noise without significant benefit |
| **Interpolate** | Time-series with temporal patterns | Not applicable — our data is transactional, not continuous time-series |

**Key Decision:** Since the raw dataset has only ~2-6% missing values (by design from the generator), dropping invalid rows preserves data integrity without significantly reducing sample size. This approach ensures all analytics are based on complete, verified records rather than estimates.

### 1. Required Fields

Rows with `NULL` values in required fields are **removed** from the dataset.

#### Trips
- `trip_id`, `user_id`, `user_type`, `bike_id`, `bike_type`
- `start_station_id`, `end_station_id`
- `start_time`, `end_time`
- `duration_minutes`, `distance_km`, `status`

#### Stations
- `station_id`, `station_name`, `capacity`
- `latitude`, `longitude`

#### Maintenance
- `record_id`, `bike_id`, `bike_type`
- `date`, `maintenance_type`, `cost`, `description`

### 2. Numeric Fields

Invalid or non-parseable numeric values are coerced to `NaN`, then filtered out.

| Field | Validation Rule |
|-------|-----------------|
| `duration_minutes` | Must be ≥ 0 |
| `distance_km` | Must be ≥ 0 |
| `capacity` | Must be ≥ 1 |
| `cost` | Must be ≥ 0 |
| `latitude` | Must be in range [-90, 90] |
| `longitude` | Must be in range [-180, 180] |

### 3. DateTime Fields

Invalid timestamps are coerced to `NaT` (Not a Time), then filtered out.

**Time Range Validation:**
- `end_time` must be ≥ `start_time`
- Trips where `end_time < start_time` are considered invalid and removed

### 4. String Fields

String fields are normalized:
- Converted to **lowercase**
- Leading/trailing **whitespace stripped**

Affected fields: `user_type`, `bike_type`, `status`, `maintenance_type`, `description`, `station_name`

### 5. Duplicates

Exact duplicate rows are **removed** after all cleaning operations.

---

## Validation Functions

### `validate_data_trips(df)`
Returns a boolean mask for valid trip rows.

**Checks:**
- All required fields are present (not null)
- `duration_minutes` ≥ 0
- `distance_km` ≥ 0
- `end_time` ≥ `start_time`

### `validate_data_stations(df)`
Returns a boolean mask for valid station rows.

**Checks:**
- All required fields are present (not null)
- `capacity` ≥ 1
- `latitude` in range [-90, 90]
- `longitude` in range [-180, 180]

### `validate_data_maintenance(df)`
Returns a boolean mask for valid maintenance rows.

**Checks:**
- All required fields are present (not null)
- `cost` ≥ 0

---

## Cleaning Functions

### `clean_data_trips(df)`
1. Converts `start_time` and `end_time` to datetime
2. Converts `duration_minutes` and `distance_km` to numeric
3. Normalizes string fields (`user_type`, `bike_type`, `status`)
4. Removes duplicates
5. Applies validation mask

### `clean_data_stations(df)`
1. Converts `capacity`, `latitude`, `longitude` to numeric
2. Strips whitespace from `station_name`
3. Removes duplicates
4. Applies validation mask

### `clean_data_maintenance(df)`
1. Converts `date` to datetime
2. Converts `cost` to numeric
3. Normalizes string fields (`maintenance_type`, `description`)
4. Removes duplicates
5. Applies validation mask

---

## Data Flow

```
Raw CSV Data
     │
     ▼
┌─────────────┐
│   Loading   │  (loader.py)
└─────────────┘
     │
     ▼
┌─────────────┐
│  Cleaning   │  (utils.py: clean_data_*)
└─────────────┘
     │
     ▼
┌─────────────┐
│ Validation  │  (utils.py: validate_data_*)
└─────────────┘
     │
     ▼
┌─────────────┐
│   Mapping   │  (mapper.py: dataframe_to_*)
└─────────────┘
     │
     ▼
  Domain Objects (models.py)
```