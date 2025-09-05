import customtkinter as ctk
import json
import datetime
# import os # No longer needed for file path checking

# --- Configuration ---
# JSON_FILE_PATH = 'test_data.json' # No longer needed
WINDOW_TITLE = "Domain Expiry Checker (Paste JSON)"
WINDOW_SIZE = "500x600" # Increased size for input box

# --- GUI Application Class ---
class DomainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)

        # --- Widgets ---

        # Input Area for JSON
        self.json_input_label = ctk.CTkLabel(self, text="Paste JSON data here:")
        self.json_input_label.pack(pady=(10, 5), padx=20, anchor="w") # Align left

        self.json_input_textbox = ctk.CTkTextbox(self, height=200) # Added height
        self.json_input_textbox.pack(pady=5, padx=20, fill="both", expand=True) # Fill available space

        # Button to trigger processing
        self.process_button = ctk.CTkButton(self, text="Process Pasted JSON", command=self.process_pasted_json)
        self.process_button.pack(pady=10)

        # Output Area for Results
        self.result_label = ctk.CTkLabel(self, text="Valid Domains (Not Expired & Unique):")
        self.result_label.pack(pady=(10, 5), padx=20, anchor="w") # Align left

        self.result_textbox = ctk.CTkTextbox(self, height=250) # Adjusted height
        self.result_textbox.pack(pady=10, padx=20, fill="both", expand=True) # Fill available space
        self.result_textbox.configure(state="disabled") # Make it read-only initially

    def process_pasted_json(self):
        """Processes JSON from the input textbox, filters domains, and displays them."""
        self.result_textbox.configure(state="normal") # Enable writing to output
        self.result_textbox.delete("1.0", ctk.END) # Clear previous results

        domains_to_display = []
        error_message = None

        # Get JSON string from the input textbox
        json_string = self.json_input_textbox.get("1.0", ctk.END).strip() # Get all text and remove whitespace

        if not json_string:
            error_message = "Error: Please paste JSON data into the input box."
        else:
            try:
                # Parse the JSON string
                data = json.loads(json_string) # Use json.loads for string

                # Get current date
                today = datetime.datetime.now().date()
                unique_domains = set()

                # --- Start of your original processing logic (slightly adapted) ---
                search_results = data.get('search_result', []) # Use .get for safety
                if not isinstance(search_results, list):
                     error_message = "Error: 'search_result' in JSON is not a list or is missing."
                else:
                    for domain_data in search_results:
                        # Check if domain_data is a dictionary before accessing keys
                        if not isinstance(domain_data, dict):
                            print(f"Warning: Skipping non-dictionary item in search_result: {domain_data}")
                            continue

                        expiry_date_str = domain_data.get('expiry_date')
                        domain_name = domain_data.get('domain_name')

                        if domain_name is None:
                             print(f"Warning: Skipping item with missing 'domain_name': {domain_data}")
                             continue # Skip if no domain name

                        if expiry_date_str is not None:
                            try:
                                # Attempt to parse the date
                                expiry_date = datetime.datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                                # Compare with today's date
                                if expiry_date >= today:
                                    # Add to set if unique
                                    if domain_name not in unique_domains:
                                        unique_domains.add(domain_name)
                            except ValueError:
                                print(f"Warning: Skipping domain '{domain_name}' due to invalid date format: '{expiry_date_str}'")
                            except TypeError:
                                 print(f"Warning: Skipping domain '{domain_name}' due to invalid date type: '{expiry_date_str}'")
                # --- End of original processing logic ---

                # Prepare the list for display only if no error occurred during parsing/basic structure check
                if error_message is None:
                    domains_to_display = sorted(list(unique_domains))

            except json.JSONDecodeError as e:
                error_message = f"Error: Invalid JSON data pasted.\nDetails: {e}"
            except Exception as e: # Catch other potential errors during processing
                error_message = f"An unexpected error occurred during processing: {e}"

        # --- Update Output Textbox ---
        if error_message:
            self.result_textbox.insert(ctk.END, error_message)
        elif not domains_to_display:
            self.result_textbox.insert(ctk.END, "No valid domains found matching the criteria in the pasted JSON.")
        else:
            display_string = "\n".join(domains_to_display)
            self.result_textbox.insert(ctk.END, display_string)

        self.result_textbox.configure(state="disabled") # Make output read-only again

# --- Main Execution ---
if __name__ == "__main__":
    # Set appearance mode (optional)
    # ctk.set_appearance_mode("System") # Options: "System" (default), "Dark", "Light"
    # ctk.set_default_color_theme("blue") # Options: "blue" (default), "green", "dark-blue"

    app = DomainApp()
    app.mainloop()
