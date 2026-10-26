# MATH1604 Group Project

This project analyses responses from a 100-question multiple-choice Python quiz to investigate whether the quiz answer sequence follows a hidden pattern.

## Repository Structure

- `data/`
  - Stores downloaded respondent files.

- `scripts/`
  - Contains Python modules and integration scripts.

- `output/`
  - Stores collated files and generated answer sequences.

- `reviews/`
  - Contains Jupyter notebook reviews for each team member.

## Team Modules

### M1 — Data Extraction (Daren Liby)
File:

```python
data_extraction_M1.py
```

Functions:

- `extract_answers_sequence()`
- `write_answers_sequence()`

Purpose:

- Extract answer sequences from raw respondent files.

---

### M2 — Data Preparation (Abdullah Lafi Alanazi)

File:

```python
data_preparation_M2.py
```

Functions:

- `download_answer_files()`
- `collate_answer_files()`

Purpose:

- Download and collate respondent files.

---

### M3 — Data Analysis (Zikril Hakim Bin Shahrol Hanizam)

File:

```python
data_analysis_M3.py
```

Functions:

- `generate_means_sequence()`
- `visualize_data()`

Purpose:

- Compute statistics and create visualisations.

---

### M4 — Full Integration (Haoran Yang)

File:

```python
run_full_analysis_M4.py
```

Purpose:

- Run the complete analysis workflow.

## Running the Project

Open terminal:

```bash
cd scripts
python run_full_analysis_M4.py
```

## Expected Outputs

Generated files include:

```text
data/answers_respondent_1.txt
...
data/answers_respondent_64.txt

output/collated_answers.txt

output/answer_sequences/
```

## Technologies Used

- Python
- pathlib
- urllib
- matplotlib
- GitHub
