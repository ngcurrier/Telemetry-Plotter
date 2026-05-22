import pandas as pd
import numpy as np

def generate_test_csv(filename="test_flight_data.csv"):
    n_samples = 1000
    # Variable frequency: time steps are not perfectly uniform
    t = np.cumsum(np.random.normal(0.01, 0.001, n_samples))
    t = t - t[0] # Start at 0
    
    # Some signals
    # 1. Sine wave 1Hz
    signal_1hz = np.sin(2 * np.pi * 1.0 * t)
    # 2. Sine wave 10Hz + noise
    signal_10hz_noisy = np.sin(2 * np.pi * 10.0 * t) + np.random.normal(0, 0.5, n_samples)
    # 3. Random walk (altitude-ish)
    altitude = 1000 + np.cumsum(np.random.normal(0, 0.1, n_samples))
    
    df = pd.DataFrame({
        "timestamp_sec": t,
        "control_cycle_ms": t * 1000,
        "accel_x": signal_1hz,
        "accel_y_noisy": signal_10hz_noisy,
        "altitude_ft": altitude,
        "engine_rpm": 2000 + 500 * np.sin(0.1 * t)
    })
    
    df.to_csv(filename, index=False)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_test_csv()
