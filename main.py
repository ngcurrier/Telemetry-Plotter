import sys
from data_engine import DataEngine
from plot_engine import PlotEngine
from cli_utils import CLIUtils

def main():
    de = DataEngine()
    pe = PlotEngine(de)
    cu = CLIUtils()
    
    current_y_keys = []
    
    while True:
        choice = cu.print_menu(de.x_col, current_y_keys)
        
        if choice == '1':
            file_path = cu.list_and_select_files()
            if not file_path:
                file_path = input("Enter CSV file path manually: ")
            
            if not file_path:
                continue

            try:
                keys = de.load_csv(file_path)
                print(f"Loaded {len(keys)} columns from {file_path}.")
                current_y_keys = [] # Reset on new file load
            except Exception as e:
                print(f"Error loading CSV: {e}")
        
        elif choice == '2':
            if de.df is None:
                print("Load a CSV first.")
                continue
            query = input("Search query for Y-axis (empty for all): ")
            selected = cu.search_and_select(de.get_keys(), query)
            if selected:
                if selected in current_y_keys:
                    current_y_keys.remove(selected)
                    print(f"Removed {selected}")
                else:
                    current_y_keys.append(selected)
                    print(f"Added {selected}")
        
        elif choice == '3':
            if de.df is None:
                print("Load a CSV first.")
                continue
            query = input("Search query for X-axis: ")
            selected = cu.search_and_select(de.get_keys(), query)
            if selected:
                de.set_x_column(selected)
                print(f"X-Axis column set to {selected}. Estimated 'frequency': {de.fs:.2f}")
        
        elif choice == '4':
            if not current_y_keys:
                print("Select at least one Y-axis first.")
                continue
            pe.plot_line(current_y_keys)
        
        elif choice == '5':
            if not current_y_keys:
                print("Select at least one Y-axis first.")
                continue
            pe.plot_fft(current_y_keys)
        
        elif choice == '6':
            if not current_y_keys:
                print("Select at least one Y-axis first.")
                continue
            pe.plot_spectrogram(current_y_keys)
        
        elif choice == '7':
            if not current_y_keys:
                print("Select a Y-axis first. (Filter applies to all selected)")
                continue
            f_choice = cu.print_filter_menu()
            new_keys = []
            for k in current_y_keys:
                try:
                    if f_choice == '1':
                        cutoff = float(input(f"Enter cutoff frequency (Hz) for {k}: "))
                        new_keys.append(de.butter_lowpass_filter(k, cutoff))
                    elif f_choice == '2':
                        cutoff = float(input(f"Enter cutoff frequency (Hz) for {k}: "))
                        new_keys.append(de.butter_highpass_filter(k, cutoff))
                    elif f_choice == '3':
                        window = int(input(f"Enter moving average window size for {k}: "))
                        new_keys.append(de.moving_average(k, window))
                except Exception as e:
                    print(f"Error filtering {k}: {e}")
            if new_keys:
                print(f"Created new columns: {', '.join(new_keys)}")
                current_y_keys = new_keys
            input("\nPress Enter to continue...")
        
        elif choice == '8':
            if not current_y_keys:
                print("Select a Y-axis first.")
                continue
            for k in current_y_keys:
                stats = de.get_stats(k)
                print(f"\nStats for {k}:")
                if "error" in stats:
                    print(f"  {stats['error']}")
                else:
                    for s_k, s_v in stats.items():
                        print(f"  {s_k}: {s_v}")
            input("\nPress Enter to continue...")
        
        elif choice == '9':
            if de.df is None:
                print("Load a CSV first.")
                continue
            file_path = input("Enter output CSV path: ")
            if de.save_csv(file_path):
                print(f"Saved to {file_path}")
            else:
                print("Error saving CSV.")

        elif choice == '0':
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
