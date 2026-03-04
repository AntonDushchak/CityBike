# CityBike Analytics Suite

## Overview

CityBike is a compact analytics and reporting pipeline for bike-sharing datasets. The project ingests raw CSV files (stations, trips, maintenance), cleans them with pandas, and orchestrates insights, visualizations, algorithm demos, and benchmark reports from a single entry point.

## Key Features

- **Data Cleaning & Validation** – Normalizes timestamps, numeric fields, and categorical columns; filters invalid or duplicate entries before analysis.
- **Analytics Reporter** – Answers the Unit 10–11 business questions (trip totals, top stations, peak hours, user segments, maintenance KPIs, outliers, etc.) using pandas and NumPy.
- **Automated Reporting** – Generates `output/summary_report.txt` plus CSV extracts (`top_stations.csv`, `top_users.csv`, `maintenance_costs.csv`, `maintenance_frequency.csv`).
- **Visualizations** – Saves Matplotlib PNG charts to `output/figures/` (bar, line, histogram, box plot, and benchmark comparison).
- **Custom Algorithms Showcase** – Applies `my_sort`/`my_search` to real trip and station records and compares them against Python/pandas implementations via `timeit` (results + chart).

## Project Structure

```
CityBike/
├── data/                      # raw CSV inputs
├── analytics_reporter.py      # metric calculations & report builder
├── analyzer.py                # BikeShareSystem orchestration layer
├── visualization.py           # Matplotlib helpers (Agg backend)
├── algorithms.py              # custom sort/search + benchmarks
├── utils.py                   # data cleaning functions
├── loader.py                  # CSV I/O helpers
├── main.py                    # entry point (run pipeline end-to-end)
└── output/                    # generated reports/figures (gitignored)
```

## Getting Started

1. **Create & activate a virtual environment** (optional but recommended).
	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```
2. **Install dependencies.**
	```powershell
	pip install -r requirements.txt
	```
3. **Run the pipeline.**
	```powershell
	python main.py
	```
	The script prints paths of generated artifacts and writes deliverables under `output/`.

## Outputs

- `output/summary_report.txt` – Full textual analytics summary.
- `output/*.csv` – Tables for top stations, top users, and maintenance KPIs.
- `output/figures/*.png` – Required Matplotlib visualizations plus the algorithm benchmark chart.

## Customization Tips

- Replace the CSVs in `data/` with your own bike-share datasets (keep column names consistent with `utils.py`).
- Modify `visualization.py` to add new charts; `BikeShareSystem.generate_figures()` will automatically pick them up if you append to the list.
- Tune benchmark sample sizes in `BikeShareSystem.benchmark_algorithms()` if you need faster/slower comparisons.

## Requirements

See [requirements.txt](requirements.txt) for the exact dependency list used by the pipeline.