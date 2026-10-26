# IMDb Movie Rating Analysis by Zikril Hakim

## Project Overview

An independent data science project analysing 5,000 IMDb movies using Python to investigate relationships between movie ratings, popularity, runtime, genres, and release years.

## Objectives

- Explore the distribution of IMDb movie ratings.

- Investigate relationships between movie ratings and popularity.

- Analyse trends across movie genres and decades.

- Develop and evaluate machine learning models to estimate IMDb ratings.

## Technologies Used

- Python

- Pandas and NumPy

- Matplotlib

- Scikit-learn

- Google Colab

## Key Findings

- 11.22% of movies received ratings of 8.0 or higher.

- IMDb ratings and vote counts showed a moderate positive correlation (r = 0.39).

- Runtime showed a weak positive correlation with ratings (r = 0.28).

- Release year showed a weak negative correlation with ratings (r = -0.27).

## Machine Learning

Linear Regression and Random Forest models were used to estimate IMDb movie ratings. Additional genre features were introduced using one-hot encoding.

Model performance was evaluated using Mean Absolute Error (MAE) and R².

## Limitations

The dataset contains a selected sample of 5,000 movies and may not represent all IMDb titles. Correlations do not establish causation, and differences in sample sizes across decades may introduce selection bias.
