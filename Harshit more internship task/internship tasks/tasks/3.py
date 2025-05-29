import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("C:/Users/venom/Desktop/internship task/Play Store Data.csv")

# Clean 'Installs' column: Remove non-numeric characters and convert to int
df["Installs"] = (
    df["Installs"]
    .replace({r'[^\d]': ''}, regex=True)  # Remove symbols (e.g., commas, '+', etc.)
    .replace('', '0')  # Replace empty strings with '0'
    .astype(float)  # Convert to float (handles NaN)
    .astype(int)  # Convert to int
)

# Convert 'Last Updated' column to datetime format
df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

# Ensure 'Reviews' is numeric
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0)

# Filter data: Apps with Installs >= 10M, Rating >= 4.0, Last Updated in January
df_filtered = df[
    (df["Installs"] >= 10_000_000) &
    (df["Rating"] >= 4.0) &
    (df["Last Updated"].dt.month == 1)
]

# Get top 10 categories by installs
top_categories = df_filtered.groupby("Category")["Installs"].sum().sort_values(ascending=False).head(10)
df_top = df_filtered[df_filtered["Category"].isin(top_categories.index)]

# Aggregate average rating and total review count per category
df_grouped = df_top.groupby("Category").agg({
    "Rating": "mean",
    "Reviews": "sum"
}).reset_index()

# Normalize Reviews to match Rating scale (so they are visually aligned)
df_grouped["Reviews_Normalized"] = df_grouped["Reviews"] / df_grouped["Reviews"].max() * 5  # Scale to max 5 (same as Rating)

# Create figure
fig = go.Figure()

# Add Rating bars
fig.add_trace(go.Bar(
    x=df_grouped["Category"],
    y=df_grouped["Rating"],
    name="Average Rating",
    marker_color="blue"
))

# Add Reviews bars (Normalized)
fig.add_trace(go.Bar(
    x=df_grouped["Category"],
    y=df_grouped["Reviews_Normalized"],
    name="Total Reviews (Scaled)",
    marker_color="red"
))

# Update layout
fig.update_layout(
    title="Comparison of Average Rating and Total Reviews for Top 10 App Categories",
    xaxis=dict(title="Category"),
    yaxis=dict(title="Value (Ratings & Scaled Reviews)"),
    barmode="group"  # Ensures bars are side by side
)

# Save the figure as an HTML file
fig.write_html("C:/Users/venom/Desktop/internship task/Task_3.html")

print("Chart saved as HTML file successfully!")
