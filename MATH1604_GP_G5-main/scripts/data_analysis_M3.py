from pathlib import Path
import matplotlib.pyplot as plt

try:
    from data_extraction_M1 import extract_answers_sequence
except ImportError:
    from scripts.data_extraction_M1 import extract_answers_sequence


def generate_means_sequence(collated_answers_path):
    """
    Compute mean answer value for each question.
    """

    path = Path(collated_answers_path)

    if not path.exists():
        raise FileNotFoundError("Collated file not found")

    content = path.read_text(encoding="utf-8", errors="ignore")

    sections = content.split("\n*\n")

    all_answers = []

    for i, section in enumerate(sections):
        temp_file = f"temp_{i}.txt"

        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(section)

        answers = extract_answers_sequence(temp_file)
        all_answers.append(answers)

    means = []

    for q in range(100):
        values = [ans[q] for ans in all_answers if ans[q] != 0]

        if len(values) > 0:
            means.append(sum(values) / len(values))
        else:
            means.append(0)

    return means


def visualize_data(collated_answers_path, n):
    """
    Plot data.
    """

    means = generate_means_sequence(collated_answers_path)

    x = list(range(1, 101))

    if n == 1:
        plt.scatter(x, means)
        plt.title("Mean Answer Value per Question")
        plt.xlabel("Question")
        plt.ylabel("Mean Answer")
        plt.show()

    elif n == 2:
        plt.plot(x, means)
        plt.title("Mean Answer Trend")
        plt.xlabel("Question")
        plt.ylabel("Mean Answer")
        plt.show()

    else:
        print("Error: n must be 1 or 2")
