## exercise_app

import streamlit as st
import pandas as pd
import os
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

# Display editable table
edited_df = st.data_editor(
    df,
    column_config={
        "Date": st.column_config.TextColumn(disabled=True),
        "Hours": st.column_config.TextColumn(),  # Editable
        "Score": st.column_config.NumberColumn(disabled=True)  # Auto-calculated
    },
    num_rows="dynamic"  # Allows adding new rows if needed
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

# Display updated data

st.write(df)

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
