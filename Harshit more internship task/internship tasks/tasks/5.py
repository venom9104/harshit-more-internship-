import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("C:/Users/venom/Desktop/internship task/Play Store Data.csv")

# Clean 'Installs' column by removing '+' and ',' and converting to numeric
df["Installs"] = df["Installs"].str.replace(r'[+,]', '', regex=True)
df["Installs"] = pd.to_numeric(df["Installs"], errors='coerce')

# Convert 'Last Updated' column to datetime (accounting for the specific format)
df["Last Updated"] = pd.to_datetime(df["Last Updated"], format='%B %d, %Y', errors='coerce')

# Ensure 'Reviews' is numeric
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

# Drop NaN values
df = df.dropna(subset=["Installs", "Reviews", "Last Updated", "Category"])

# Apply filtering conditions
df_filtered = df[
    (~df["App"].str.startswith(("X", "Y", "Z"), na=False)) &  # Exclude apps starting with X, Y, Z
    (df["Category"].str.startswith(("E", "C", "B"), na=False)) &  # Apps starting with E, C, B
    (df["Reviews"] > 500)  # More than 500 reviews
]

# Convert 'Year-Month' from 'Last Updated' to Timestamp
df_filtered["Year-Month"] = df_filtered["Last Updated"].dt.to_period("M").dt.to_timestamp()

# Aggregate installs by Year-Month and Category
df_grouped = df_filtered.groupby(["Year-Month", "Category"])["Installs"].sum().reset_index()

# Calculate month-over-month growth
df_grouped["Prev Month Installs"] = df_grouped.groupby("Category")["Installs"].shift(1)
df_grouped["Growth (%)"] = ((df_grouped["Installs"] - df_grouped["Prev Month Installs"]) / df_grouped["Prev Month Installs"]) * 100
df_grouped["Significant Growth"] = df_grouped["Growth (%)"] > 20  # Mark areas with >20% growth

# Fill NaN values in growth calculations
df_grouped.fillna(0, inplace=True)

# Create the line plot
fig = px.line(
    df_grouped,
    x="Year-Month",
    y="Installs",
    color="Category",
    title="Total Installs Trend by App Category",
    labels={"Installs": "Installs", "Year-Month": "Time"}
)

# Highlight significant growth areas
for _, row in df_grouped[df_grouped["Significant Growth"]].iterrows():
    if row["Growth (%)"] > 20:  # Only shade areas with > 20% growth
        fig.add_traces(
            go.Scatter(
                x=[row["Year-Month"], row["Year-Month"]],
                y=[0, row["Installs"]],
                fill='tozeroy',  # This fills the area under the line
                fillcolor='rgba(0, 255, 0, 0.3)',  # Green color with some transparency
                line=dict(color='green', width=0),  # No border for the fill
                mode='lines',  # Only the fill area, no line drawn
                showlegend=False  # Hide this trace from the legend
            )
        )
# Save as HTML file
fig.write_html("C:/Users/venom/Desktop/internship task/task_5.html")
print("Chart saved as task_5.html")
print(df_filtered.head())  # Check filtered data
print(df_grouped.head())  # Check grouped data
