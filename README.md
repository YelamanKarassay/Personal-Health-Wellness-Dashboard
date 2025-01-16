# Personal Health & Wellness Dashboard

Link: [Dashboard](https://daily-wellness-dashboard.streamlit.app/)

A **Streamlit**-based dashboard for visualizing and analyzing personal daily data—weight, mood, meals, sleep, and more. This project uses **pandas**, **plotly**, **matplotlib**, **seaborn**, **scikit-learn**, and **wordcloud** to present insights about your health and daily habits.

## Table of Contents

1. [Project Overview](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#project-overview)
2. [Features](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#features)
3. [Project Structure](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#project-structure)
4. [Installation & Setup](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#installation--setup)
5. [Usage](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#usage)
6. [Future Developments](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#future-developments)
7. [License (MIT)](https://chatgpt.com/c/67888c4b-bbc4-800d-99d4-f73c88385192#license-mit)

---

## Project Overview

This dashboard helps you visualize various personal metrics—such as **Weight**, **Feelings (Morning/Evening)**, **Sleep**, **Meals**, **Weather**, and more—on a daily, weekly, and monthly basis. It also includes correlation analyses, word clouds for categorical data (e.g., meals, weather), and a basic “optimal values” section that uses polynomial regression to suggest an ideal sleep duration for improved mood.

---

## Features

1. **Daily (Overall) Overview**
    
    - Line charts for Weight, Feel Morning, Feel Evening, Feel Average, and Air Quality.
    - Phrase Clouds for Weather, Breakfast, Lunch, and Dinner.
    - Bar chart for Sleep Duration and Sleep Debt.
2. **Weekly Overview**
    
    - Aggregated weekly charts showing the same metrics as Daily, but averaged or summed by week.
3. **Monthly Overview**
    
    - Similar to Weekly but aggregated by month.
4. **Correlation Analysis**
    
    - Correlation matrix (heatmap) for numeric features.
    - Scatter plots with an optional regression line for any selected pair of variables.
5. **Optimal Values**
    
    - A simple polynomial regression model that estimates the optimal Sleep Duration for maximizing Feel Average.

---

## Project Structure

```
├── app.py               # Main Streamlit application
├── daily_data.csv       # Example CSV file with user data
├── README.md            # Project README
└── requirements.txt     # (Optional) List of Python dependencies
```

- **app.py**: Contains the primary code for loading, preprocessing, and visualizing data in Streamlit.
- **daily_data.csv**: Example data file; replace or update it with your own.
- **requirements.txt**: (Optional) For listing dependencies.

---

## Installation & Setup

1. **Clone this repository** or download the source code.
    
2. **Install Python 3.7+** (if not already installed).
    
3. **Install dependencies**:
    
    ```bash
    pip install streamlit pandas numpy plotly seaborn matplotlib scikit-learn wordcloud
    ```
    
    Or, if you have a `requirements.txt`, do:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Place your CSV data** (e.g., `daily_data.csv`) in the project root or edit the file path in `app.py` to point to your data.
    

---

## Usage

1. **Open a terminal** in the project directory.
    
2. **Run Streamlit**:
    
    ```bash
    streamlit run app.py
    ```
    
3. **Open your browser** (if it doesn’t open automatically) at the address shown in your terminal, typically `http://localhost:8501`.
    
4. **Explore the dashboard**:
    
    - **Daily (Overall) Overview**: Detailed daily charts and phrase clouds.
    - **Weekly Overview**: Aggregated weekly charts.
    - **Monthly Overview**: Aggregated monthly charts.
    - **Correlation**: Correlation matrix and scatter plots.
    - **Optimal Values**: Displays a polynomial regression to find an approximate best sleep duration for mood.

---

## Future Developments

You might consider enhancing this project with:

- **Time-Series Forecasting** (Prophet, ARIMA, LSTM) to predict future weight, mood, or sleep.
- **Anomaly Detection** (Isolation Forest, DBSCAN) to spot unusual days.
- **Mood Prediction** with Machine Learning (Random Forest, Gradient Boosting, etc.).
- **Nutritional Analysis** if you add calorie or macro data for each meal.
- **Goal/Target Tracking** for personal habit consistency.
- **Advanced Weather Integration** (e.g., temperature, humidity, AQI) for deeper correlation insights.
---

Thank you for exploring this Personal Health & Wellness Dashboard. If you have any questions, issues, or suggestions, feel free to open an issue or submit a pull request! Enjoy your data exploration.