import json
import argparse
from pathlib import Path

def merge_jsonl_files(input_files, output_file):
    """
    Merge multiple JSONL files into a single JSONL file.
    
    Args:
        input_files (list): List of paths to input JSONL files
        output_file (str): Path to the output merged JSONL file
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for input_file in input_files:
            try:
                with open(input_file, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        # Verify each line is valid JSON
                        try:
                            json.loads(line.strip())
                            outfile.write(line)
                        except json.JSONDecodeError as e:
                            print(f"Warning: Skipping invalid JSON in {input_file}: {e}")
            except Exception as e:
                print(f"Error processing file {input_file}: {e}")

def main():
    input_files = [
        "results/2025-01-25b.jsonl",
        "results/2025-01-29.jsonl",
        "results/2025-01-29bb.jsonl",
        "results/2025-01-30.jsonl",
        "results/merged.jsonl"
    ]
    output_file = [
        "results/merged2.jsonl"
    ]
    merge_jsonl_files(input_files, output_file[0])
if __name__ == "__main__":
    main()