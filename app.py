import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

############################################
# 1) DATA LOADING AND PREP
############################################

def load_data(csv_path="daily_data.csv"):
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    
    # Create new feature: Feel Average
    df["Feel Average"] = (df["Feeling Morning"] + df["Feeling Evening"]) / 2

    # Interpolate Sleep if you like:
    df["Sleep Duration"] = df["Sleep Duration"].interpolate()
    df["Sleep Debt"] = df["Sleep Debt"].interpolate()

    return df

############################################
# HELPER: PHRASE CLOUD
############################################

def generate_phrase_cloud_from_frequencies(series, title="Phrase Cloud"):
    """
    Takes a Pandas Series of 'phrases' (e.g. "Japanese Curry", "Subway Egg & Mayo")
    and generates a WordCloud treating each entire phrase as a single token.
    The size of each phrase depends on its frequency in the Series.
    """
    freq_dict = series.value_counts().dropna().to_dict()  # {phrase: count}
    if len(freq_dict) == 0:
        # If there's no data, just return an empty figure
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data available", ha='center', va='center')
        ax.axis("off")
        return fig

    wc = WordCloud(
        background_color="white", 
        collocations=False  # Important for preventing internal splitting
    ).generate_from_frequencies(freq_dict)

    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    ax.set_title(title)
    return fig

############################################
# HELPER: CHARTING FUNCTIONS
############################################

def line_chart(df, x_col, y_col, chart_title):
    fig = px.line(df, x=x_col, y=y_col, title=chart_title)
    st.plotly_chart(fig)

def bar_chart_multiple(df, x_col, y_cols, chart_title, barmode="group"):
    fig = px.bar(df, x=x_col, y=y_cols, barmode=barmode, title=chart_title)
    st.plotly_chart(fig)

############################################
# 2) DAILY (OVERALL) VIEW
############################################

def daily_view(df):
    st.subheader("Daily (Overall) Overview")

    # 1.1 Weight over Date (Line Graph)
    st.write("**Weight over Date**")
    line_chart(df, "Date", "Weight", "Weight over Date")

    # 1.2 Weather Phrase Cloud
    st.write("**Weather Phrase Cloud**")
    fig_weather = generate_phrase_cloud_from_frequencies(df["Weather"], "Weather Phrases")
    st.pyplot(fig_weather)

    # 1.3 Feel Morning over Date (Line Graph)
    st.write("**Feel Morning over Date**")
    line_chart(df, "Date", "Feeling Morning", "Feel Morning over Date")

    # 1.4 Feel Evening over Date (Line Graph)
    st.write("**Feel Evening over Date**")
    line_chart(df, "Date", "Feeling Evening", "Feel Evening over Date")

    # 1.5 Feel Average over Date (Line Graph)
    st.write("**Feel Average over Date**")
    line_chart(df, "Date", "Feel Average", "Feel Average over Date")

    # 1.6 Air over Date (Line Graph)
    st.write("**Air over Date**")
    line_chart(df, "Date", "Air", "Air over Date")

    # 1.7 Breakfast Phrase Cloud
    st.write("**Breakfast Phrase Cloud**")
    fig_breakfast = generate_phrase_cloud_from_frequencies(df["Breakfast"], "Breakfast Phrases")
    st.pyplot(fig_breakfast)

    # 1.8 Lunch Phrase Cloud
    st.write("**Lunch Phrase Cloud**")
    fig_lunch = generate_phrase_cloud_from_frequencies(df["Lunch"], "Lunch Phrases")
    st.pyplot(fig_lunch)

    # 1.9 Dinner Phrase Cloud
    st.write("**Dinner Phrase Cloud**")
    fig_dinner = generate_phrase_cloud_from_frequencies(df["Dinner"], "Dinner Phrases")
    st.pyplot(fig_dinner)

    # 1.10 Sleep Duration and Sleep Debt Over Date (Bar Chart)
    st.write("**Sleep Duration & Sleep Debt Over Date**")
    bar_chart_multiple(
        df, 
        x_col="Date", 
        y_cols=["Sleep Duration", "Sleep Debt"], 
        chart_title="Sleep Duration and Sleep Debt Over Date"
    )

############################################
# 3) WEEKLY OVERVIEW
############################################

def weekly_overview(df):
    st.subheader("Weekly Overview")
    # Group data by ISO week
    df["Week"] = df["Date"].dt.isocalendar().week

    weekly_df = df.groupby("Week", dropna=False).agg({
        "Weight": "mean",
        "Feeling Morning": "mean",
        "Feeling Evening": "mean",
        "Feel Average": "mean",
        "Air": "mean",
        "Sleep Duration": "mean",
        "Sleep Debt": "mean"
    }).reset_index()

    #  - Weight line
    st.write("**Weekly Avg Weight**")
    line_chart(weekly_df, "Week", "Weight", "Weekly Average Weight")

    #  - Weather phrase cloud aggregated for entire dataset (week-by-week clouds would require a filter).
    #    For demonstration, let's make a single phrase cloud of all week's weather. 
    #    If you truly want a "Week-by-week" word cloud, you'd add a selectbox for a specific week.
    st.write("**(Optional) Single Weather Phrase Cloud for entire data**")
    fig_weather = generate_phrase_cloud_from_frequencies(df["Weather"], "Weather Phrases (All Weeks)")
    st.pyplot(fig_weather)

    #  - Feel Morning line
    st.write("**Weekly Avg Feel Morning**")
    line_chart(weekly_df, "Week", "Feeling Morning", "Weekly Average Feel Morning")

    #  - Feel Evening line
    st.write("**Weekly Avg Feel Evening**")
    line_chart(weekly_df, "Week", "Feeling Evening", "Weekly Average Feel Evening")

    #  - Feel Average line
    st.write("**Weekly Avg Feel Average**")
    line_chart(weekly_df, "Week", "Feel Average", "Weekly Average Feel Average")

    #  - Air line
    st.write("**Weekly Avg Air**")
    line_chart(weekly_df, "Week", "Air", "Weekly Average Air")

    #  - Breakfast phrase cloud (overall data, or do a filter for a specific week)
    st.write("**(Optional) Single Breakfast Phrase Cloud for entire data**")
    fig_breakfast = generate_phrase_cloud_from_frequencies(df["Breakfast"], "Breakfast Phrases (All Weeks)")
    st.pyplot(fig_breakfast)

    #  - Lunch phrase cloud
    st.write("**(Optional) Single Lunch Phrase Cloud for entire data**")
    fig_lunch = generate_phrase_cloud_from_frequencies(df["Lunch"], "Lunch Phrases (All Weeks)")
    st.pyplot(fig_lunch)

    #  - Dinner phrase cloud
    st.write("**(Optional) Single Dinner Phrase Cloud for entire data**")
    fig_dinner = generate_phrase_cloud_from_frequencies(df["Dinner"], "Dinner Phrases (All Weeks)")
    st.pyplot(fig_dinner)

    #  - Sleep Duration & Debt (line or bar)
    st.write("**Weekly Avg Sleep Duration & Sleep Debt**")
    bar_chart_multiple(
        weekly_df, 
        x_col="Week", 
        y_cols=["Sleep Duration", "Sleep Debt"], 
        chart_title="Weekly Average Sleep Duration & Sleep Debt"
    )

############################################
# 4) MONTHLY OVERVIEW
############################################

def monthly_overview(df):
    st.subheader("Monthly Overview")
    # Group data by month
    df["Month"] = df["Date"].dt.month

    monthly_df = df.groupby("Month", dropna=False).agg({
        "Weight": "mean",
        "Feeling Morning": "mean",
        "Feeling Evening": "mean",
        "Feel Average": "mean",
        "Air": "mean",
        "Sleep Duration": "mean",
        "Sleep Debt": "mean"
    }).reset_index()

    #  - Weight line
    st.write("**Monthly Avg Weight**")
    line_chart(monthly_df, "Month", "Weight", "Monthly Average Weight")

    #  - Weather phrase cloud (overall data again)
    st.write("**(Optional) Single Weather Phrase Cloud for entire data**")
    fig_weather = generate_phrase_cloud_from_frequencies(df["Weather"], "Weather Phrases (All Months)")
    st.pyplot(fig_weather)

    #  - Feel Morning line
    st.write("**Monthly Avg Feel Morning**")
    line_chart(monthly_df, "Month", "Feeling Morning", "Monthly Average Feel Morning")

    #  - Feel Evening line
    st.write("**Monthly Avg Feel Evening**")
    line_chart(monthly_df, "Month", "Feeling Evening", "Monthly Average Feel Evening")

    #  - Feel Average line
    st.write("**Monthly Avg Feel Average**")
    line_chart(monthly_df, "Month", "Feel Average", "Monthly Average Feel Average")

    #  - Air line
    st.write("**Monthly Avg Air**")
    line_chart(monthly_df, "Month", "Air", "Monthly Average Air")

    #  - Breakfast phrase cloud
    st.write("**(Optional) Single Breakfast Phrase Cloud for entire data**")
    fig_breakfast = generate_phrase_cloud_from_frequencies(df["Breakfast"], "Breakfast Phrases (All Months)")
    st.pyplot(fig_breakfast)

    #  - Lunch phrase cloud
    st.write("**(Optional) Single Lunch Phrase Cloud for entire data**")
    fig_lunch = generate_phrase_cloud_from_frequencies(df["Lunch"], "Lunch Phrases (All Months)")
    st.pyplot(fig_lunch)

    #  - Dinner phrase cloud
    st.write("**(Optional) Single Dinner Phrase Cloud for entire data**")
    fig_dinner = generate_phrase_cloud_from_frequencies(df["Dinner"], "Dinner Phrases (All Months)")
    st.pyplot(fig_dinner)

    #  - Sleep Duration & Debt
    st.write("**Monthly Avg Sleep Duration & Sleep Debt**")
    bar_chart_multiple(
        monthly_df,
        x_col="Month",
        y_cols=["Sleep Duration", "Sleep Debt"],
        chart_title="Monthly Average Sleep Duration & Sleep Debt"
    )

############################################
# 5) CORRELATION SECTION
############################################

def correlation_section(df):
    st.subheader("Correlation")

    numeric_cols = [
        "Weight",
        "Feeling Morning",
        "Feeling Evening",
        "Feel Average",
        "Air",
        "Sleep Duration",
        "Sleep Debt"
    ]

    # 4.1 Correlation Matrix
    st.write("**Correlation Matrix**")
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # Below the matrix, let user pick two variables for a scatter plot + regression
    st.write("**Scatter Plot & Regression**")
    x_var = st.selectbox("Select X variable", numeric_cols, index=0)
    y_var = st.selectbox("Select Y variable", numeric_cols, index=1)

    if x_var and y_var:
        fig_scatter = px.scatter(df, x=x_var, y=y_var, trendline="ols",
                                 title=f"{x_var} vs {y_var} with Regression")
        st.plotly_chart(fig_scatter)

############################################
# 6) OPTIMAL VALUES
############################################

def optimal_values_section(df):
    """
    Attempt to find an overall "optimal" Sleep Duration for maximizing Feel Average.
    We'll do a simple polynomial regression of degree=2: 
    Feel Average ~ a*(Sleep Duration)^2 + b*(Sleep Duration) + c
    Then find vertex of the parabola.
    """
    st.subheader("Optimal Values - Sleep Duration to Maximize Feel Average")

    # Prepare data
    sub_df = df.dropna(subset=["Sleep Duration", "Feel Average"])
    X = sub_df[["Sleep Duration"]].values
    y = sub_df["Feel Average"].values

    if len(X) < 3:
        st.write("Not enough data to perform polynomial regression.")
        return

    # Fit polynomial of degree 2
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    # Coefficients: FeelAvg = c + b*Sleep + a*Sleep^2
    c = model.intercept_
    b = model.coef_[1]
    a = model.coef_[2]

    st.write(f"Polynomial Model: FeelAverage = {a:.3f}*Sleep^2 + {b:.3f}*Sleep + {c:.3f}")

    # If 'a' != 0, the vertex is at x = -b / (2a)
    # That's the "optimal" Sleep Duration for maximum or minimum
    if a == 0:
        st.write("Coefficient a=0, so the relationship is linear, not quadratic.")
        # If b > 0 => more sleep better, if b < 0 => less sleep better
        # We can just show a scatter with regression line
        slope_direction = "Positive" if b > 0 else "Negative"
        st.write(f"Slope is {slope_direction}. No single 'optimal' point in a strictly linear sense.")
    else:
        x_opt = -b / (2*a)
        st.write(f"**Optimal Sleep Duration** (vertex of parabola) = {x_opt:.2f} hours")

    # Let's plot the curve
    sleep_min = np.min(X)
    sleep_max = np.max(X)
    sleep_range = np.linspace(sleep_min, sleep_max, 100).reshape(-1,1)
    sleep_range_poly = poly.transform(sleep_range)
    pred_range = model.predict(sleep_range_poly)

    fig_opt, ax_opt = plt.subplots()
    ax_opt.scatter(X, y, alpha=0.5, label="Actual Data")
    ax_opt.plot(sleep_range, pred_range, color="red", label="Polynomial Fit")
    ax_opt.set_xlabel("Sleep Duration (hrs)")
    ax_opt.set_ylabel("Feel Average")
    ax_opt.set_title("Feel Average vs Sleep Duration (Polynomial Regression)")
    ax_opt.legend()
    st.pyplot(fig_opt)

############################################
# MAIN STREAMLIT APP
############################################

def main():
    st.title("My Dashboard")

    df = load_data()  # Load your CSV

    menu = [
        "Daily (Overall) Overview",
        "Weekly Overview",
        "Monthly Overview",
        "Correlation",
        "Optimal Values"
    ]
    choice = st.sidebar.selectbox("Select a Section", menu)

    if choice == "Daily (Overall) Overview":
        daily_view(df)
    elif choice == "Weekly Overview":
        weekly_overview(df)
    elif choice == "Monthly Overview":
        monthly_overview(df)
    elif choice == "Correlation":
        correlation_section(df)
    elif choice == "Optimal Values":
        optimal_values_section(df)

if __name__ == "__main__":
    main()
