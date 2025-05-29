import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("C:/Users/venom/Desktop/internship task/Play Store Data.csv")

# Convert 'Last Updated' to datetime
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Filter for apps updated between 2017 and 2018
df_filtered = df[(df['Last Updated'].dt.year >= 2017) & (df['Last Updated'].dt.year <= 2018)]

# Convert 'Installs' to numeric (removing commas and plus signs)
df_filtered.loc[:, 'Installs'] = df_filtered['Installs'].str.replace(',', '').str.replace('+', '').astype(float)

# Convert 'Reviews' to numeric
df_filtered.loc[:, 'Reviews'] = pd.to_numeric(df_filtered['Reviews'], errors='coerce')

# Apply filters for installs and reviews
df_filtered = df_filtered[(df_filtered['Installs'] >= 100000) & (df_filtered['Reviews'] > 1000)]

# Filter by Category (should NOT start with A, F, E, G, I, or K)
df_filtered = df_filtered[~df_filtered['Category'].str.startswith(('A', 'F', 'E', 'G', 'I', 'K'), na=False)]

# Compute correlation matrix
correlation_matrix = df_filtered[['Installs', 'Reviews']].corr()

# Convert correlation matrix to long format for Plotly
correlation_df = correlation_matrix.stack().reset_index()
correlation_df.columns = ['Variable 1', 'Variable 2', 'Correlation']

# Create interactive heatmap using Plotly
fig = px.imshow(
    correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    color_continuous_scale="viridis",
    text_auto=".2f",
    title="Interactive Correlation Heatmap",
)

# Save the interactive heatmap as an HTML file
heatmap_html_path = "C:/Users/venom/Desktop/internship task/task_6.html"
fig.write_html(heatmap_html_path)

print(f"Interactive heatmap saved as {heatmap_html_path}")
