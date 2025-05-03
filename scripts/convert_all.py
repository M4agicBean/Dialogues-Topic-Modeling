import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from conversion_utils import timestamps_preprocessing, speakers_preprocessing

RAW_DIR = "data/movies_raw/format_type_1"
PROCESSED_DIR = "data/movies_processed"

for subdir, _, files in os.walk(RAW_DIR):
    for filename in files:
        if not filename.endswith(".txt"):
            continue

        if "_speakers" not in filename and "_timestamps" not in filename:
            continue

        full_path = os.path.join(subdir, filename)

        movie_name = os.path.basename(subdir)

        output_folder = os.path.join(PROCESSED_DIR, movie_name)
        os.makedirs(output_folder, exist_ok=True)

        if "_speakers" in filename:
            try:
                df = speakers_preprocessing(full_path)
                df.to_csv(os.path.join(output_folder, "speakers.csv"), index=False)
                print(f"speakers.csv saved for: {movie_name}")
            except Exception as e:
                print(f"Error processing speakers for {movie_name}: {e}")

        elif "_timestamps" in filename:
            try:
                df = timestamps_preprocessing(full_path)
                df.to_csv(os.path.join(output_folder, "timestamps.csv"), index=False)
                print(f"timestamps.csv saved for: {movie_name}")
            except Exception as e:
                print(f"Error processing timestamps for {movie_name}: {e}")

print("\nAll files processed.")