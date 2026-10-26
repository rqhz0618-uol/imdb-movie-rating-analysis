"""
run_full_analysis_M4.py

Integration script for the MATH1604 group project.

This script runs the complete project pipeline:
1. download answer files;
2. collate raw files;
3. extract and save structured answer sequences;
4. compute mean answer values;
5. produce visualisations.
"""

from pathlib import Path

from data_preparation_M2 import download_answer_files, collate_answer_files
from data_extraction_M1 import extract_answers_sequence, write_answers_sequence
from data_analysis_M3 import generate_means_sequence, visualize_data


def main():
    """
    Run the complete MATH1604 analysis pipeline.

    Parameters
    ----------
    None

    Returns
    -------
    None
        Creates data and output files, prints summary information, and displays
        visualisations.
    """
    project_root = Path(__file__).resolve().parent.parent
    data_folder = project_root / "data"
    output_folder = project_root / "output"

    cloud_url = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
    total_respondents = 64

    print("Step 1: Downloading files...")
    downloaded = download_answer_files(cloud_url, str(data_folder), total_respondents)
    print(f"Successfully downloaded {len(downloaded)} files.")

    print("Step 2: Collating files...")
    collated_file = collate_answer_files(str(data_folder))
    print(f"Collated file created at: {collated_file}")

    print("Step 3: Extracting structured answer sequences...")
    sequences_folder = output_folder / "answer_sequences"
    sequences_folder.mkdir(parents=True, exist_ok=True)

    for respondent_id in downloaded:
        raw_file = data_folder / f"answers_respondent_{respondent_id}.txt"
        answers = extract_answers_sequence(str(raw_file))
        write_answers_sequence(answers, respondent_id, str(sequences_folder))

    print("Step 4: Computing mean sequence...")
    means = generate_means_sequence(collated_file)
    print("First 10 mean values:")
    print(means[:10])

    print("Step 5: Creating visualisations...")
    visualize_data(collated_file, 1)
    visualize_data(collated_file, 2)

    print("Full analysis complete.")


if __name__ == "__main__":
    main()
