import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import spectrogram

class PlotEngine:
    def __init__(self, data_engine):
        self.de = data_engine

    def plot_line(self, col_names):
        if isinstance(col_names, str):
            col_names = [col_names]
            
        for col in col_names:
            if self.de.x_col is None:
                plt.plot(self.de.df[col], label=col)
                plt.xlabel("Index")
            else:
                plt.plot(self.de.df[self.de.x_col], self.de.df[col], label=col)
                plt.xlabel(self.de.x_col)
        
        plt.ylabel("Value")
        plt.title(f"Plot vs {self.de.x_col if self.de.x_col else 'Index'}")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_fft(self, col_names):
        if isinstance(col_names, str):
            col_names = [col_names]

        if self.de.fs is None:
            print("Error: X-axis column not set or not numeric.")
            return

        fig, (ax_fft, ax_raw) = plt.subplots(2, 1, figsize=(10, 8), sharex=False)
        
        for col in col_names:
            t, y, fs = self.de.resample_if_needed(col)
            n = len(y)
            yf = np.fft.fft(y)
            xf = np.fft.fftfreq(n, 1/fs)[:n//2]
            
            ax_fft.plot(xf, 2.0/n * np.abs(yf[0:n//2]), label=col)
            ax_raw.plot(t, y, label=col)
        
        ax_fft.set_xlabel("Frequency (Hz)")
        ax_fft.set_ylabel("Magnitude")
        ax_fft.set_title("FFT Comparison")
        ax_fft.legend()
        ax_fft.grid(True)
        
        ax_raw.set_xlabel(f"{self.de.x_col} (s)" if 'ms' in self.de.x_col.lower() else self.de.x_col)
        ax_raw.set_ylabel("Value")
        ax_raw.set_title("Raw Signal (Time Domain)")
        ax_raw.legend()
        ax_raw.grid(True)
        
        plt.tight_layout()
        plt.show()

    def plot_spectrogram(self, col_names):
        if isinstance(col_names, str):
            col_names = [col_names]

        if self.de.fs is None:
            print("Error: X-axis column not set or not numeric.")
            return

        for col in col_names:
            t, y, fs = self.de.resample_if_needed(col)
            f, t_spec, Sxx = spectrogram(y, fs)
            
            fig, (ax_spec, ax_raw) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
            
            im = ax_spec.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
            ax_spec.set_ylabel('Frequency (Hz)')
            ax_spec.set_title(f"Spectrogram: {col}")
            fig.colorbar(im, ax=ax_spec, label='Intensity [dB]')
            
            ax_raw.plot(t, y)
            ax_raw.set_ylabel("Value")
            ax_raw.set_xlabel(f"{self.de.x_col} (s)" if 'ms' in self.de.x_col.lower() else self.de.x_col)
            ax_raw.set_title("Raw Signal")
            ax_raw.grid(True)
            
            plt.tight_layout()
        plt.show()
