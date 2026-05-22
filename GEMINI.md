# Flight Data Analysis Tool

## Overview
A professional CLI tool for analyzing flight data from CSV files. Supports variable-frequency data, signal processing, and multiple visualization types.

## Architecture
- `main.py`: Entry point, orchestrates the CLI loop.
- `data_engine.py`: Handles data loading, frequency estimation (relative to X), filtering, moving averages, and statistics.
- `plot_engine.py`: Provides Line (Y vs X), FFT, and Spectrogram plotting with automatic resampling for non-uniform data.
- `cli_utils.py`: Interactive CLI utilities including paginated key search and selection for both X and Y axes.

## Key Features
- **Compressed File Support**: Directly load and analyze `.zip` and `.gz` compressed CSV files.
- **General X-Axis Support**: Plot any two variables against each other (e.g., Engine RPM vs Altitude).
- **Key Search & Selection**: Search through thousands of keys and select by integer index. Pagination supported.
- **Variable Sampling Support**: Estimates sampling frequency relative to the selected X-axis column.
- **Descriptive Naming**: Modified data columns are automatically named based on the operation (e.g., `accel_lp_5Hz`).
- **Data Export**: Save modified datasets with new columns back to CSV.

## Installation & Dependencies
The tool requires several Python libraries for data processing and visualization. These are listed in `requirements.txt`:
- **pandas**: Data manipulation and CSV loading.
- **numpy**: Numerical operations and FFT.
- **scipy**: Signal processing (Butterworth filters, spectrograms).
- **matplotlib**: X11-based plotting and subplots.

Install them using pip:
```bash
pip install -r requirements.txt
```

## Usage
1. Generate test data: `python3 generate_test_data.py`
2. Run tool: `python3 main.py`
3. Load CSV (Option 1).
4. Select X-Axis (Option 3). If the column name contains 'ms', the tool automatically scales to Hz/Seconds.
5. Select one or more Y-Axes (Option 2).
6. Analyze via Plotting, FFT, Spectrogram, or Statistics.

## Validation
Run `python3 validate_tool.py` to verify the core filtering and statistics logic.
