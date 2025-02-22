import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from datetime import date, datetime
import pytz
import matplotlib.dates as mdates

# Set the Midwest time zone (Central Time)
midwest_tz = pytz.timezone('US/Central')

# File path
FILE_PATH = "exercise_data.csv"

# Load existing data or create a new one
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    # Initialize DataFrame with today's date in Midwest time zone
    today_midwest = datetime.now(midwest_tz).strftime('%Y-%m-%d')
    df = pd.DataFrame(columns=["Date", "Hours", "Score"])
    df = pd.concat([df, pd.DataFrame([{'Date': today_midwest,  'Score': 0, 'Hours': '' }])], ignore_index=True)

# Convert to datetime and fill missing dates
try:
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize('UTC').dt.tz_convert(midwest_tz)
    all_dates = pd.date_range(df['Date'].min(), pd.Timestamp.today(tz=midwest_tz), freq='D')
    missing_dates = all_dates.difference(df['Date'])
    for d in missing_dates:
        df = pd.concat([df, pd.DataFrame([{'Date': d, 'Score': 0, 'Hours': '' }])], ignore_index=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')  # Store dates as strings for CSV compatibility
except Exception as e:
    st.error(f"Error processing dates: {e}")
    df = pd.DataFrame([{'Date': date.today().strftime('%Y-%m-%d'), 'Score': 0,  'Hours': ''}])

# Ensure proper data types
df["Hours"] = df["Hours"].astype(str)
df = df.sort_values('Date', ascending=False).reset_index(drop=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.write("### Exercise Log")
    
    # Pre-fill new rows with today's date in Midwest time zone
    today_midwest = datetime.now(midwest_tz).strftime('%Y-%m-%d')
    if df.empty or df.iloc[0]['Date'] != today_midwest:
        df = pd.concat([pd.DataFrame([{'Date': today_midwest, 'Score': 0,  'Hours': '' }]), df], ignore_index=True)

    edited_df = st.data_editor(
        df,
        column_config={
            "Date": st.column_config.TextColumn(disabled=True),
            "Score": st.column_config.NumberColumn(disabled=True),
            "Hours": st.column_config.TextColumn()
        },
        num_rows="dynamic"
    )
    # Filter out empty rows
    edited_df = edited_df[edited_df['Date'].astype(bool)]
    # Update values in original dataframe
    for _, row in edited_df.iterrows():
        date_str = row['Date']
        hours_str = row['Hours']
        try:
            hours = float(hours_str) if hours_str.strip() else 0
        except:
            hours = 0
            
        score = round(hours / 3, 2)
        df.loc[df['Date'] == date_str, ['Score',  'Hours' ]] = [score, hours_str]

with col2:
    # Display updated data
    st.write("### Updated Data")
    st.write(df[["Date","Score",   "Hours"]])

######plot
st.write("### Analysis & Trends")
# Convert Date to numerical format for regression analysis
df["Date_Num"] = pd.to_datetime(df["Date"]).map(pd.Timestamp.toordinal)
df = df.sort_values("Date_Num")
# Filter out empty scores
df = df[df["Score"] > 0]
if len(df) > 1:
    X = df["Date_Num"].values.reshape(-1, 1)
    y = df["Score"].values
    # --- Linear Regression ---
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    y_pred_linear = lin_reg.predict(X)
    r2_linear = r2_score(y, y_pred_linear)
    # --- Polynomial Regression (Degree 2) ---
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    poly_reg = LinearRegression()
    poly_reg.fit(X_poly, y)
    y_pred_poly = poly_reg.predict(X_poly)
    r2_poly = r2_score(y, y_pred_poly)
    # --- SINGLE PLOT ---
    fig, ax = plt.subplots(figsize=(10, 6))
    # Scatter plot with dashed line connecting actual points
    sns.scatterplot(x=pd.to_datetime(df["Date"]), y=df["Score"], ax=ax, color="blue", label="Actual Scores")
    ax.plot(pd.to_datetime(df["Date"]), df["Score"], linestyle="dashed", color="blue", alpha=0.6)
    # Linear regression line
    ax.plot(pd.to_datetime(df["Date"]), y_pred_linear, color="red", label=f"Linear Fit (R²={r2_linear:.3f})")
    # Polynomial regression line
    ax.plot(pd.to_datetime(df["Date"]), y_pred_poly, color="green", label=f"Polynomial Fit (R²={r2_poly:.3f})")
    # Grid lines
    ax.grid(True, linestyle="--", alpha=0.6)  # Add dashed grid with transparency
    ax.set_title("Score Analysis: Actual Data, Linear & Polynomial Regression")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score")
    ax.legend()
    
    # Format the X-axis to show a label every 7 days
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
    ax.tick_params(axis='x', rotation=45)
    # Show plot in Streamlit
    st.pyplot(fig)
else:
    st.warning("Not enough data for regression analysis. Enter more scores!")
##################################################
import streamlit as st
from boy_image import create_boy_image

# Set up the Streamlit app
st.write("====================================")
st.write("Who am I:")

# Generate the resized boy image
boy_image = create_boy_image()

# Define the new dimensions (width, height)
new_width = 100
new_height = 150

# Define the original and larger dimensions
original_width, original_height = 100, 150  # Original size
larger_width, larger_height = 600, 800      # Larger size

# Resize the image to the original size
resized_boy_image = boy_image.resize((original_width, original_height))

# Display the original-sized image
st.image(resized_boy_image, caption="This is me!", use_container_width=False)

# Add a button to show the larger image
if st.button("Show Larger Image"):
    # Resize the image to the larger size
    larger_boy_image = boy_image.resize((larger_width, larger_height))
    
    # Display the larger image
    st.image(larger_boy_image, caption="This is me (larger)!", use_container_width=False)
