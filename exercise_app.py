## exercise_app

import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from datetime import date

# File path
FILE_PATH = "exercise_data.csv"

# Load existing data or create a new one
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=["Date", "Hours", "Score"])

# Ensure "Date" column is a string
df["Date"] = df["Date"].astype(str)

# Get today's date
today = date.today().strftime("%Y-%m-%d")

# Check if today's date is already in the file
if today not in df["Date"].values:
    # Append a new row for today
    new_entry = pd.DataFrame([{"Date": today, "Hours": "", "Score": 0}])
    df = pd.concat([df, new_entry], ignore_index=True)

# Ensure "Hours" is treated as a string to allow blank input
df["Hours"] = df["Hours"].astype(str)

# Create two text areas side-by-side
col1, col2 = st.columns(2)
with col1:
    st.write("### Exercise Log")
with col2:
    st.write("### Analysis & Trends")

# Editable table
edited_df = st.data_editor(
    df,
    column_config={
        "Date": st.column_config.TextColumn(disabled=True),
        "Hours": st.column_config.TextColumn(),  # Editable
        "Score": st.column_config.NumberColumn(disabled=True)  # Auto-calculated
    },
    num_rows="dynamic"
)

# Update dataframe with user input
for i, row in edited_df.iterrows():
    try:
        hours = float(row["Hours"]) if row["Hours"].strip() else 0
    except ValueError:
        hours = 0  # Handle invalid input

    df.at[i, "Hours"] = row["Hours"]
    df.at[i, "Score"] = hours / 3  # Auto-update score

# Save updated data back to CSV
df.to_csv(FILE_PATH, index=False)

# Convert Date to numerical format for regression analysis
df["Date_Num"] = pd.to_datetime(df["Date"]).map(pd.Timestamp.toordinal)
df = df.sort_values("Date_Num")  # Ensure sorted order

# Filter out empty scores
df = df[df["Score"] > 0]

# Ensure enough data for regression
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

    # --- PLOTTING ---
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # 1. Score vs. Date
    sns.scatterplot(x=df["Date"], y=df["Score"], ax=axs[0], color="blue")
    axs[0].set_title("Score vs. Date")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("Score")
    axs[0].tick_params(axis='x', rotation=45)

    # 2. Linear Regression
    sns.scatterplot(x=df["Date"], y=df["Score"], ax=axs[1], color="blue", label="Actual Scores")
    axs[1].plot(df["Date"], y_pred_linear, color="red", label=f"Linear Fit (R²={r2_linear:.3f})")
    axs[1].set_title("Linear Regression Analysis")
    axs[1].set_xlabel("Date")
    axs[1].set_ylabel("Score")
    axs[1].legend()
    axs[1].tick_params(axis='x', rotation=45)

    # 3. Polynomial Regression
    sns.scatterplot(x=df["Date"], y=df["Score"], ax=axs[2], color="blue", label="Actual Scores")
    axs[2].plot(df["Date"], y_pred_poly, color="green", label=f"Polynomial Fit (R²={r2_poly:.3f})")
    axs[2].set_title("Polynomial Regression Analysis (Degree 2)")
    axs[2].set_xlabel("Date")
    axs[2].set_ylabel("Score")
    axs[2].legend()
    axs[2].tick_params(axis='x', rotation=45)

    # Show plots in Streamlit
    st.pyplot(fig)

else:
    st.warning("Not enough data for regression analysis. Enter more scores!")

# Display updated data
st.write("### Updated Data")
st.write(df[["Date", "Hours", "Score"]])

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
