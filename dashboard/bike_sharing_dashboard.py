import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
# # Load cleaned data
# cleaned_day = pd.read_csv(r"C:\submission\dashboard\cleaned_day.csv")
# cleaned_hour = pd.read_csv(r"C:\submission\dashboard\cleaned_hour.csv")
cleaned_day = pd.read_csv("cleaned_day.csv")
cleaned_hour = pd.read_csv("cleaned_hour.csv")

# Convert 'dteday' to datetime
cleaned_day['dteday'] = pd.to_datetime(cleaned_day['dteday'])
cleaned_hour['dteday'] = pd.to_datetime(cleaned_hour['dteday'])

# Dashboard Title
st.title("Bike Sharing Dashboard")

st.sidebar.image("bike-removebg-preview.png", use_column_width=True)

# Add a date range filter
st.sidebar.header("Date Range Filter")
min_date = cleaned_day['dteday'].min()
max_date = cleaned_day['dteday'].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter data based on selected date range
filtered_day = cleaned_day[(cleaned_day['dteday'] >= pd.to_datetime(start_date)) & (cleaned_day['dteday'] <= pd.to_datetime(end_date))]
filtered_hour = cleaned_hour[(cleaned_hour['dteday'] >= pd.to_datetime(start_date)) & (cleaned_hour['dteday'] <= pd.to_datetime(end_date))]

# Create a pivot table to get total rentals by hour
pivot_table_hourly_rentals = filtered_hour.groupby(filtered_hour['hr'])['total_rentals'].sum().reset_index()
pivot_table_hourly_rentals.columns = ['hour', 'total_rentals']

# Determine the peak hour (highest rentals)
peak_time = pivot_table_hourly_rentals.loc[pivot_table_hourly_rentals['total_rentals'].idxmax(), 'hour']

# Visualization for Total Bike Rentals by Hour
st.subheader("Total Bike Rentals by Hour In A Day (Visualization Q1)")

fig, ax = plt.subplots(figsize=(12, 6))
plt.bar(pivot_table_hourly_rentals['hour'], pivot_table_hourly_rentals['total_rentals'], color='skyblue')
plt.title('Total Bike Rentals by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Total Rentals')
plt.xticks(pivot_table_hourly_rentals['hour'])
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Highlight the peak time
plt.axvline(x=peak_time, color='red', linestyle='--', label=f'Peak Time: {peak_time}:00')
plt.legend()
plt.tight_layout()

# Display the plot in the Streamlit app
st.pyplot(fig)

# Visualization 2: Total Bike Rentals by Date (Line Chart)
st.subheader("Total Bike Rentals by Date in a certain time")

# Create a pivot table to get total rentals by day, renaming 'cnt' to 'total_rentals'
pivot_table_daily_rentals = filtered_day.groupby('dteday')['total_rentals'].sum().reset_index()

# Plot the line chart
fig2, ax2 = plt.subplots(figsize=(12, 6))
plt.plot(pivot_table_daily_rentals['dteday'], pivot_table_daily_rentals['total_rentals'], marker='o', color='green')
plt.title('Total Bike Rentals by Date')
plt.xlabel('Date')
plt.ylabel('Total Rentals')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot in the Streamlit app
st.pyplot(fig2)

# Group by month and calculate average rentals for 'casual' and 'registered' users
average_rentals_by_month = filtered_day.groupby(filtered_day['dteday'].dt.month)[['casual_users', 'registered_users']].mean()

# Visualization: Average Bike Rentals by Month (Bar Chart)
st.subheader("Average Bike Rentals by Month (Visualization Q2)")

# Set up the figure
fig3, ax = plt.subplots(figsize=(10, 6))

# Create a bar plot for average rentals by month
average_rentals_by_month.plot(kind='bar', color=['skyblue', 'orange'], ax=ax)

# Add titles and labels
ax.set_title('Average Bike Rentals by Month', fontsize=16)
ax.set_xlabel('Month', fontsize=14)
ax.set_ylabel('Average Rentals', fontsize=14)
ax.set_xticklabels(average_rentals_by_month.index, rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add a legend
ax.legend(['Casual Users', 'Registered Users'], title='User Type')

# Adjust layout to prevent clipping
plt.tight_layout()

# Display the plot in the Streamlit app
st.pyplot(fig3)

# Visualization: Pie Chart for Average Bike Rentals by User Type
st.subheader("Average Bike Rentals Distribution (Casual vs Registered)")

# Calculate total average rentals for each user type
total_average_rentals = average_rentals_by_month[['casual_users', 'registered_users']].mean()

# Set up the pie chart
fig4, ax = plt.subplots(figsize=(8, 8))

# Create the pie chart
ax.pie(total_average_rentals, labels=['Casual Users', 'Registered Users'], autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange'])

# Equal aspect ratio ensures that pie chart is a circle
ax.axis('equal')  

# Add a title
plt.title('Average Bike Rentals Distribution by User Type', fontsize=16)

# Display the plot in the Streamlit app
st.pyplot(fig4)