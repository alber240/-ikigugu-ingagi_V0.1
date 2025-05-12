# Importing the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Define the project timeline in a dictionary
project_data = {
    'Task': ['Setup Project', 'Define System Flow', 'Database Schema Design', 'Tech Stack Setup', 'API Design'],
    'Start Date': ['2025-05-12', '2025-05-13', '2025-05-14', '2025-05-15', '2025-05-16'],
    'End Date': ['2025-05-12', '2025-05-13', '2025-05-14', '2025-05-15', '2025-05-16']
}

# Convert the start and end dates to datetime objects for plotting
project_data['Start Date'] = pd.to_datetime(project_data['Start Date'])
project_data['End Date'] = pd.to_datetime(project_data['End Date'])

# Create a DataFrame from the project data
df = pd.DataFrame(project_data)

# Plotting the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through the data to plot each task on the chart
for i, task in df.iterrows():
    ax.barh(task['Task'], (task['End Date'] - task['Start Date']).days, left=task['Start Date'])

# Formatting the x-axis to show date values properly
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Set labels for x and y axes
plt.xlabel('Date')
plt.ylabel('Task')

# Title of the Gantt chart
plt.title('Project Timeline')

# Display the plot
plt.tight_layout()
plt.show()
