from data_engine import DataEngine
import os

def validate():
    de = DataEngine()
    test_csv = "test_flight_data.csv"
    
    if not os.path.exists(test_csv):
        print("Test CSV not found. Generating...")
        import generate_test_data
        generate_test_data.generate_test_csv()

    print(f"Loading {test_csv}...")
    keys = de.load_csv(test_csv)
    print(f"Keys: {keys}")
    
    print("Setting X-axis column...")
    de.set_x_column("timestamp_sec")
    print(f"Estimated 'frequency': {de.fs}")
    
    print("Applying Butterworth filter to accel_y_noisy...")
    new_key = de.butter_lowpass_filter("accel_y_noisy", 5.0)
    print(f"Created key: {new_key}")
    
    print("Applying High-pass filter...")
    hp_key = de.butter_highpass_filter("accel_y_noisy", 40.0)
    print(f"Created key: {hp_key}")
    
    print("Applying Moving Average...")
    ma_key = de.moving_average("accel_y_noisy", 10)
    print(f"Created key: {ma_key}")

    print("Computing stats for original, filtered, hp, and ma...")
    orig_stats = de.get_stats("accel_y_noisy")
    filt_stats = de.get_stats(new_key)
    hp_stats = de.get_stats(hp_key)
    ma_stats = de.get_stats(ma_key)
    
    print(f"Original std: {orig_stats['std']:.4f}")
    print(f"LP Filtered std: {filt_stats['std']:.4f}")
    print(f"HP Filtered std: {hp_stats['std']:.4f}")
    print(f"MA std: {ma_stats['std']:.4f}")
    
    if filt_stats['std'] < orig_stats['std'] and ma_stats['std'] < orig_stats['std']:
        print("Validation SUCCESS: Filters reduced noise.")
    else:
        print("Validation FAILURE.")

if __name__ == "__main__":
    validate()
