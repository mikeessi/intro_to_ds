import json
import os
import csv


# Directory containing the JSON files
directory = "/Users/chengyuanfang/Downloads/HY/IDS/mini project/yliopistot/filtered"

# List to hold the combined data
combined_data = []

# Dictionary to map filenames to university names in Finnish
university_mapping = {
    "aalto-yliopisto.json": "Aalto-yliopisto",
    "helsingin yliopisto.json": "Helsingin yliopisto",
    "ita-suomen yliopisto.json": "Itä-Suomen yliopisto",
    "jyvaskylan yliopisto.json": "Jyväskylän yliopisto",
    "lapin yliopisto.json": "Lapin yliopisto",
    "lappeenrannan teknillinen yliopisto.json": "Lappeenrannan teknillinen yliopisto",
    "maanpuolustuskorkeakoulu.json": "Maanpuolustuskorkeakoulu",
    "oulun yliopisto.json": "Oulun yliopisto",
    "svenska hogskolan.json": "Svenska högskolan",
    "taideyliopisto.json": "Taideyliopisto",
    "tampereen yliopisto.json": "Tampereen yliopisto",
    "turun yliopisto.json": "Turun yliopisto",
    "vaasan yliopisto.json": "Vaasan yliopisto",
    "abo akademi.json": "Åbo Akademi"
}

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        # Construct the full path to the file
        file_path = os.path.join(directory, filename)
        university_name = university_mapping.get(filename, "Tuntematon yliopisto")  # Default if name not in dictionary
        
        with open(file_path, "r", encoding="utf-8") as file:
            # Read the file line by line to handle multiple JSON objects
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if line:  # Process only non-empty lines
                    try:
                        entry = json.loads(line)
                        
                        # Check if "kand" is in the major's name (for bachelor's programs)
                        if "kand" in entry["name"]:
                            # Remove "kand" from the major's name and clean up extra spaces
                            entry["name"] = entry["name"].replace("kand.", "").strip()

                            # Add the university name as a new column
                            entry["yliopisto"] = university_name

                            # Append the processed entry to the combined data
                            combined_data.append(entry)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {filename}: {e}")
                        continue

# Save the combined data to a new JSON file
output_file = os.path.join(directory, "yliopisto_hakijat_combined.json")
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(combined_data, outfile, indent=4, ensure_ascii=False)

print(f"Combined JSON file created successfully at {output_file}.")

# Define the CSV file path
output_csv_file = os.path.join(directory, "yliopisto_hakijat_combined.csv")

# List of CSV column headers (adjust according to your JSON structure)
csv_headers = ["yliopisto", "year", "name", "students"]  # Modify if needed

# Write the combined data to a CSV file
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

    # Write header
    writer.writeheader()

    # Write rows
    for entry in combined_data:
        # Filter the fields to include in the CSV (modify keys if needed)
        writer.writerow({
            "yliopisto": entry.get("yliopisto"),
            "year": entry.get("year"),
            "name": entry.get("name"),
            "students": entry.get("students")  # Adjust field names if different in JSON
        })

print(f"Combined CSV file created successfully at {output_csv_file}.")