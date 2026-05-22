import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt, resample
import logging
import zipfile
import io

class DataEngine:
    def __init__(self):
        self.df = None
        self.x_col = None
        self.fs = None

    def load_csv(self, file_path):
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as z:
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if not csv_files:
                    raise ValueError("No CSV files found in the zip archive.")
                # Load the first CSV found
                with z.open(csv_files[0]) as f:
                    self.df = pd.read_csv(f)
                    print(f"Extracted and loaded {csv_files[0]} from {file_path}")
        elif file_path.endswith('.gz'):
            self.df = pd.read_csv(file_path, compression='gzip')
            print(f"Loaded Gzip-compressed file: {file_path}")
        else:
            self.df = pd.read_csv(file_path)
        return list(self.df.columns)

    def set_x_column(self, col_name):
        if col_name not in self.df.columns:
            raise ValueError(f"Column {col_name} not found.")
        self.x_col = col_name
        self.estimate_frequency()

    def estimate_frequency(self):
        if self.x_col is None:
            return None
        
        diffs = pd.to_numeric(self.df[self.x_col], errors='coerce').diff().dropna()
        mean_dt = diffs.mean()
        
        if mean_dt == 0 or np.isnan(mean_dt):
            self.fs = 1.0
        else:
            self.fs = 1.0 / mean_dt
            
        # If the column name suggests milliseconds, convert to Hz (1/sec)
        if 'ms' in self.x_col.lower() or 'msec' in self.x_col.lower():
            self.fs *= 1000.0
            
        return self.fs

    def get_keys(self):
        return list(self.df.columns)

    def search_keys(self, query):
        return [k for k in self.df.columns if query.lower() in k.lower()]

    def butter_lowpass_filter(self, data_col, cutoff, order=5):
        if self.fs is None:
            raise ValueError("Frequency not estimated. Select a time column first.")
        
        nyq = 0.5 * self.fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        
        new_col = f"{data_col}_lp_{cutoff}Hz"
        self.df[new_col] = filtfilt(b, a, self.df[data_col])
        return new_col

    def butter_highpass_filter(self, data_col, cutoff, order=5):
        if self.fs is None:
            raise ValueError("Frequency not estimated. Select a time column first.")
        
        nyq = 0.5 * self.fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        
        new_col = f"{data_col}_hp_{cutoff}Hz"
        self.df[new_col] = filtfilt(b, a, self.df[data_col])
        return new_col

    def moving_average(self, data_col, window_size):
        new_col = f"{data_col}_ma_{window_size}"
        self.df[new_col] = self.df[data_col].rolling(window=window_size).mean()
        return new_col

    def save_csv(self, file_path):
        if self.df is not None:
            self.df.to_csv(file_path, index=False)
            return True
        return False

    def get_stats(self, col_name):
        if col_name not in self.df.columns:
            raise ValueError(f"Column {col_name} not found.")
        series = pd.to_numeric(self.df[col_name], errors='coerce').dropna()
        if series.empty:
            return {"error": "Column contains no numeric data."}
        return {
            "mean": series.mean(),
            "std": series.std(),
            "min": series.min(),
            "max": series.max(),
            "count": series.count()
        }

    def resample_if_needed(self, col_name, target_fs=None):
        if target_fs is None:
            target_fs = self.fs
        
        t = pd.to_numeric(self.df[self.x_col], errors='coerce').values
        y = pd.to_numeric(self.df[col_name], errors='coerce').values
        
        # If milliseconds, scale t to seconds to align with Hz
        if 'ms' in self.x_col.lower() or 'msec' in self.x_col.lower():
            t = t / 1000.0

        # Remove NaNs
        mask = ~np.isnan(t) & ~np.isnan(y)
        t = t[mask]
        y = y[mask]
        
        if len(t) < 2:
            raise ValueError("Not enough data points for resampling.")

        t_uniform = np.linspace(t[0], t[-1], len(t))
        y_uniform = np.interp(t_uniform, t, y)
        
        return t_uniform, y_uniform, target_fs
