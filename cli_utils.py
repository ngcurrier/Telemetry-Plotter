import os

class CLIUtils:
    @staticmethod
    def list_and_select_files(extensions=None):
        if extensions is None:
            extensions = [".csv", ".zip", ".gz"]

        files = [f for f in os.listdir('.') if any(f.endswith(ext) for ext in extensions)]
        if not files:
            print(f"No matching files found in current directory.")
            return None
        
        print(f"\nAvailable files:")
        for idx, file in enumerate(files):
            print(f"[{idx}] {file}")
        
        try:
            selection = input("\nSelect file by index (or press Enter for manual path): ")
            if not selection:
                return None
            idx = int(selection)
            if 0 <= idx < len(files):
                return files[idx]
            else:
                print("Invalid index.")
                return None
        except ValueError:
            print("Invalid input.")
            return None

    @staticmethod
    def search_and_select(keys, query=None, page_size=20):
        if query:
            filtered_keys = [(i, k) for i, k in enumerate(keys) if query.lower() in k.lower()]
        else:
            filtered_keys = list(enumerate(keys))
        
        if not filtered_keys:
            print("No keys found matching query.")
            return None
        
        total_matches = len(filtered_keys)
        current_idx = 0
        
        while True:
            print(f"\nMatches (Showing {current_idx} to {min(current_idx + page_size, total_matches)} of {total_matches}):")
            for i in range(current_idx, min(current_idx + page_size, total_matches)):
                idx, key = filtered_keys[i]
                print(f"[{idx}] {key}")
            
            print("\nOptions: [index] to select, [n] for next page, [p] for previous, [q] to cancel")
            choice = input("Choice: ").strip().lower()
            
            if choice == 'n':
                if current_idx + page_size < total_matches:
                    current_idx += page_size
                else:
                    print("Already at the last page.")
            elif choice == 'p':
                if current_idx - page_size >= 0:
                    current_idx -= page_size
                else:
                    print("Already at the first page.")
            elif choice == 'q' or not choice:
                return None
            else:
                try:
                    selected_idx = int(choice)
                    # Check if selected_idx is in the filtered_keys (as the first element of the tuple)
                    # For simplicity, we check if it's in the full keys range
                    if 0 <= selected_idx < len(keys):
                        return keys[selected_idx]
                    else:
                        print("Invalid index.")
                except ValueError:
                    print("Invalid input.")

    @staticmethod
    def print_menu(current_x=None, current_y_list=None):
        if current_y_list is None:
            current_y_list = []
            
        print("\n--- Flight Data Analysis Tool ---")
        print("1. Load CSV")
        print("2. Add/Remove Y-Axis (Current Data)")
        print("3. Set X-Axis Column")
        print("4. Plot Y(s) vs X (Line)")
        print("5. Plot FFT")
        print("6. Plot Spectrogram")
        print("7. Filter/Manipulate Data")
        print("8. Show Statistics")
        print("9. Save CSV")
        print("0. Exit")
        print("---------------------------------")
        print(f"Current X-Axis: {current_x if current_x else 'Not Set (Defaults to Index)'}")
        y_display = ", ".join(current_y_list) if current_y_list else "None Selected"
        print(f"Current Y-Axis: {y_display}")
        return input("Choose an option: ")

    @staticmethod
    def print_filter_menu():
        print("\n--- Filter/Manipulation ---")
        print("1. Butterworth Lowpass")
        print("2. Butterworth Highpass")
        print("3. Moving Average")
        print("4. Back")
        return input("Choose an option: ")
