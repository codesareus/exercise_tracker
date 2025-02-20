## exercise_app

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
from pathlib import Path
import pytz  # For timezone handling

# Define your local timezone
LOCAL_TIMEZONE = pytz.timezone('America/Chicago')  # Replace with your local timezone

# Define activities and their exercise scores
activities = {
    "静坐30m": 0.16, 
    "慢跑5千米60m": 0.333,
    "武当压腿+活骨功20m": 0.111,
    "五行气功10m": 0.056,
    "太极5m": 0.028,
    "易筋经20m": 0.111,
    "武当八段锦20m": 0.111,
    "12段锦20m": 0.111,
    "全身拍15m": 0.083, 
    "其他20m": 0.111,
    "其他10m": 0.056,
    "其他5m": 0.028,
    "---------": 0
}

# File paths for daily and monthly data (saved in the root directory)
DAILY_DATA_FILE = "daily_data.csv"
MONTHLY_DATA_FILE = "monthly_data.csv"

# Function to load data from file
def load_data(file_path, columns):
    path = Path(file_path)  # Use Path object
    if path.exists():
        data = pd.read_csv(path)
        # Ensure all required columns are present
        for col in columns:
            if col not in data.columns:
                data[col] = None  # Add missing columns with None values
        return data
    return pd.DataFrame(columns=columns)

# Function to save data to file (updated to filter out 0 exercise scores)
def save_data(data, file_path):
    # Check if the data contains the "Total Exercise Score" column (monthly_data)
    if "Total Exercise Score" in data.columns:
        # Filter out rows where "Total Exercise Score" is 0
        filtered_data = data[data["Total Exercise Score"] != 0]
    else:
        # For daily_data, no filtering is needed
        filtered_data = data
    
    # Save the filtered (or unfiltered) data to the file
    filtered_data.to_csv(file_path, index=False)
    
# Initialize session state for storing data
if "daily_data" not in st.session_state:
    st.session_state.daily_data = load_data(DAILY_DATA_FILE, columns=["Activity", "Exercise Score", "Hour"])  # Load daily data
if "monthly_data" not in st.session_state:
    st.session_state.monthly_data = load_data(MONTHLY_DATA_FILE, columns=["Date", "Total Exercise Score"])  # Load monthly data
if "checkbox_states" not in st.session_state:
    st.session_state.checkbox_states = {activity: False for activity in activities}
if "submit_key" not in st.session_state:
    st.session_state.submit_key = 0  # Unique key to force checkbox reset
if "last_end_day_time" not in st.session_state:
    st.session_state.last_end_day_time = None  # Track the last time "End Day" was triggered
if "show_download_button" not in st.session_state:
    st.session_state.show_download_button = False  # Track whether to show the download button

# Sidebar for activity selection
st.sidebar.title("Daily Activities")
selected_activities = []
for i, (activity, score) in enumerate(activities.items()):
    # Skip rendering the checkbox for the 8th activity
    if i == 12:  # Index 7 corresponds to the 8th activity
        st.sidebar.write(activity)  # Display the activity name without a checkbox
        continue  # Skip the rest of the loop for this activity

    # Use a unique key for each checkbox to force reset
    checkbox_state = st.sidebar.checkbox(
        activity,
        value=st.session_state.checkbox_states[activity],
        key=f"{activity}_{st.session_state.submit_key}",  # Unique key
    )
    if checkbox_state:
        selected_activities.append((activity, score))

# Add a text input box for the key
key_input = st.sidebar.text_input("Enter the key to submit data:", type="password")

# Define the required key
REQUIRED_KEY = "999999999"

# Check if the entered key matches the required key
key_is_valid = key_input == REQUIRED_KEY

# Add selected activities to daily data (only if the key is valid)
if st.sidebar.button("Submit", disabled=not key_is_valid):
    if selected_activities:
        # Get the current hour in the local timezone
        current_time = datetime.now(LOCAL_TIMEZONE)
        current_hour = current_time.hour
        
        # Create a DataFrame for the selected activities
        new_data = pd.DataFrame(selected_activities, columns=["Activity", "Exercise Score"])
        new_data["Hour"] = current_hour  # Add the current hour to the DataFrame
        
        # Append new data to daily data
        st.session_state.daily_data = pd.concat([st.session_state.daily_data, new_data], ignore_index=True)
    
    # Reset all checkboxes to unchecked
    for activity in activities:
        st.session_state.checkbox_states[activity] = False
    st.session_state.submit_key += 1  # Increment the key to force checkbox reset

    # Save the updated daily data to file
    save_data(st.session_state.daily_data, DAILY_DATA_FILE)

    # Force the app to rerun immediately
    st.rerun()

# Display a message if the key is invalid
if key_input and not key_is_valid:
    st.sidebar.error("Invalid key. Please enter the correct key to submit data.")

# Display daily activity table
st.title("Daily Activity Tracker")
st.write("### Daily Activities and Exercise Scores")

# Group by "Activity" and "Hour" and sum the exercise scores
if not st.session_state.daily_data.empty and "Exercise Score" in st.session_state.daily_data.columns:
    # Group by "Activity" and "Hour" and sum the exercise scores
    grouped_data = st.session_state.daily_data.groupby(["Activity", "Hour"], as_index=False)["Exercise Score"].sum()
    
    # Round the exercise scores to 1 decimal place
    grouped_data["Exercise Score"] = grouped_data["Exercise Score"].round(3)
    
    # Sort the table by "Hour" in ascending order
    grouped_data = grouped_data.sort_values(by="Hour")
    
    # Display the grouped, formatted, and sorted table with custom column width
    st.dataframe(
        grouped_data,
        column_config={
            "Activity": st.column_config.TextColumn(
                "Activity", width="large"  # Increase the width of the "Activity" column
            ),
            "Hour": st.column_config.NumberColumn(
                "Hour", format="%d"  # Format the "Hour" column as an integer
            ),
            "Exercise Score": st.column_config.NumberColumn(
                "Exercise Score", format="%.1f"  # Format the "Exercise Score" column to 1 decimal place
            ),
        },
        use_container_width=True,  # Use the full width of the container
    )
else:
    st.write("No data available for today.")

# Calculate total daily exercise score (rounded to 1 decimal place)
if not st.session_state.daily_data.empty and "Exercise Score" in st.session_state.daily_data.columns:
    total_daily_exercise = round(st.session_state.daily_data["Exercise Score"].sum(), 1)  # Use Python's round function
    # Ensure the total daily exercise score is not negative
    total_daily_exercise = max(total_daily_exercise, 0)  # Set to 0 if negative
else:
    total_daily_exercise = 0.0  # Default value if no data is available

# Display the current daily total exercise score
st.write(f"### Current Daily Total Exercise Score: {total_daily_exercise}")

# Automatically trigger "End Day" at 5:00 PM
current_time = datetime.now(LOCAL_TIMEZONE).time()
end_day_time = time(17, 0)  # 5:00 PM

if current_time >= end_day_time and st.session_state.last_end_day_time != datetime.now(LOCAL_TIMEZONE).date():
    # Ensure the total daily exercise score is not negative
    total_daily_exercise = max(total_daily_exercise, 0)  # Set to 0 if negative
    
    # Add daily total to monthly data
    today = datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d")
    new_monthly_data = pd.DataFrame({"Date": [today], "Total Exercise Score": [total_daily_exercise]})
    st.session_state.monthly_data = pd.concat([st.session_state.monthly_data, new_monthly_data], ignore_index=True)
    st.session_state.daily_data = pd.DataFrame(columns=["Activity", "Exercise Score", "Hour"])  # Reset daily data

    # Save the updated monthly data to file
    save_data(st.session_state.monthly_data, MONTHLY_DATA_FILE)
    # Save the reset daily data to file
    save_data(st.session_state.daily_data, DAILY_DATA_FILE)

    # Update the last execution time
    st.session_state.last_end_day_time = datetime.now(LOCAL_TIMEZONE).date()

    # Set the flag to show the download button
    st.session_state.show_download_button = True

    # Force the app to rerun immediately
    st.rerun()

# Manual "End Day" button
if st.button("End Day"):
    # Ensure the total daily exercise score is not negative
    total_daily_exercise = max(total_daily_exercise, 0)  # Set to 0 if negative
    
    today = datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d")
    new_monthly_data = pd.DataFrame({"Date": [today], "Total Exercise Score": [total_daily_exercise]})
    st.session_state.monthly_data = pd.concat([st.session_state.monthly_data, new_monthly_data], ignore_index=True)
    st.session_state.daily_data = pd.DataFrame(columns=["Activity", "Exercise Score", "Hour"])  # Reset daily data

    # Save the updated monthly data to file
    save_data(st.session_state.monthly_data, MONTHLY_DATA_FILE)
    # Save the reset daily data to file
    save_data(st.session_state.daily_data, DAILY_DATA_FILE)

    # Set the flag to show the download button
    st.session_state.show_download_button = True

    # Force the app to rerun immediately
    st.rerun()

# Show the download button if the flag is set
if st.session_state.show_download_button:
    # Filter out rows with 0 exercise scores before creating the CSV
    filtered_monthly_data = st.session_state.monthly_data[st.session_state.monthly_data["Total Exercise Score"] != 0]
    
    # Convert the filtered monthly data to a CSV string
    csv = filtered_monthly_data.to_csv(index=False).encode('utf-8')

    # Create a download button for the filtered monthly data
    st.download_button(
        label="Download Monthly Data as CSV",
        data=csv,
        file_name='monthly_data.csv',
        mime='text/csv',
    )

    # Reset the flag after showing the button
    st.session_state.show_download_button = False

# Plot daily exercise levels up to the current hour
st.write("### Daily Exercise Level (4 AM to Current Time)")
if not st.session_state.daily_data.empty and "Exercise Score" in st.session_state.daily_data.columns:
    # Get the current hour of the day in the local timezone
    current_time = datetime.now(LOCAL_TIMEZONE)
    current_hour = current_time.hour

    # Define the start and end times for the plot (in the local timezone)
    start_time = LOCAL_TIMEZONE.localize(datetime(current_time.year, current_time.month, current_time.day, 4, 0))  # Start at 4 AM
    end_time = LOCAL_TIMEZONE.localize(datetime(current_time.year, current_time.month, current_time.day, 21, 0))  # End at 9 PM

    # Generate times from 4 AM to the current hour (in the local timezone)
    times = pd.date_range(start=start_time, end=current_time, freq="h")

    # Initialize exercise levels and timestamps
    exercise_levels = []
    formatted_times = []

    # Track cumulative exercise
    cumulative_exercise = 0

    # Simulate exercise accumulation based on logged activities
    for time in times:
        # Calculate the exercise score for the current hour
        hour_exercise = st.session_state.daily_data[st.session_state.daily_data["Hour"] == time.hour]["Exercise Score"].sum()
        cumulative_exercise += hour_exercise
        
        # Ensure cumulative exercise is not negative
        cumulative_exercise = max(cumulative_exercise, 0)  # Cap at 0 if negative
        
        # Append the cumulative exercise and formatted time
        exercise_levels.append(cumulative_exercise)
        
        # Format the time in the local timezone
        formatted_time = time.strftime("%I %p").lstrip("0")  # Remove leading zero and format as "4 AM"
        formatted_times.append(formatted_time)

    # Round exercise levels to 1 decimal place
    exercise_levels = np.round(exercise_levels, 1)
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 4))  # Adjust the height to 2/3 of the original
    ax.plot(formatted_times, exercise_levels, marker="o")
    ax.set_xlabel("Time of Day (St. Louis Time)")
    ax.set_ylabel("Exercise Score")
    ax.set_title("Exercise Level Up to Current Time")
    ax.grid(True)  # Add grid lines
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(fig)
else:
    st.write("No data available for today.")

# Plot monthly exercise levels
st.write("### Monthly Exercise Level")
if not st.session_state.monthly_data.empty and "Total Exercise Score" in st.session_state.monthly_data.columns:
    # Group by date and sum the exercise scores to handle duplicate entries
    monthly_data_grouped = st.session_state.monthly_data.groupby("Date", as_index=False)["Total Exercise Score"].sum()
    
    # Round monthly exercise scores to 1 decimal place
    monthly_data_grouped["Total Exercise Score"] = monthly_data_grouped["Total Exercise Score"].round(1)
    
    # Format the "Date" column to display only month and day (e.g., "10-05" for October 5)
    monthly_data_grouped["Formatted Date"] = pd.to_datetime(monthly_data_grouped["Date"]).dt.strftime("%m-%d")
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 4))  # Adjust the height to 2/3 of the original
    ax.plot(monthly_data_grouped["Formatted Date"], monthly_data_grouped["Total Exercise Score"], marker="o")
    ax.set_xlabel("Date (Month-Day)")
    ax.set_ylabel("Total Exercise Score")
    ax.set_title("Exercise Level Over the Month")
    ax.grid(True)  # Add grid lines
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(fig)
else:
    st.write("No data available for the month.")

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
