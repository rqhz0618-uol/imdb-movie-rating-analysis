"""
data_extraction_M1.py

This module extracts answer sequences from raw quiz response files.

Each question has four options. Selected answers are marked with [x].
Unanswered questions are recorded as 0.
"""

from pathlib import Path


def extract_answers_sequence(file_path):
    """
    Extract answers from a quiz response file.

    Parameters:
        file_path (str): Path to the text file

    Returns:
        list[int]: List of 100 integers (1–4 or 0)

    Raises:
        FileNotFoundError: if file does not exist
        ValueError: if format is incorrect
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("File not found")

    lines = path.read_text(encoding="utf-8").splitlines()

    answers = []
    current_question = []

    def process_question(options):
        if len(options) != 4:
            raise ValueError("Each question must have 4 options")

        selected = []

        for i, line in enumerate(options, start=1):
            if "[x]" in line.lower():
                selected.append(i)

        if len(selected) > 1:
            raise ValueError("More than one answer selected")

        if len(selected) == 0:
            return 0

        return selected[0]

    for line in lines:
        line = line.strip()

        if line.lower().startswith("question"):
            if current_question:
                answers.append(process_question(current_question))
                current_question = []

        elif line.startswith("["):
            current_question.append(line)

    # last question
    if current_question:
        answers.append(process_question(current_question))

    if len(answers) != 100:
        raise ValueError(f"Expected 100 answers, got {len(answers)}")

    return answers


def write_answers_sequence(answers, n, destination_path):
    """
    Save answers to a file.

    Parameters:
        answers (list): list of 100 integers
        n (int): respondent ID
        destination_path (str): folder path
    """

    if len(answers) != 100:
        raise ValueError("Answers must be length 100")

    for a in answers:
        if a not in [0, 1, 2, 3, 4]:
            raise ValueError("Invalid answer value")

    folder = Path(destination_path)
    folder.mkdir(parents=True, exist_ok=True)

    output_file = folder / f"answers_list_respondent_{n}.txt"

    with open(output_file, "w") as f:
        for ans in answers:
            f.write(str(ans) + "\n")
