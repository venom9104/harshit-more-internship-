import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pytz
from datetime import datetime
import nltk
nltk.download('vader_lexicon')

# Load datasets
apps_df = pd.read_csv("C:/Users/venom/Desktop/internship task/Play Store Data.csv")
reviews_df = pd.read_csv("C:/Users/venom/Desktop/internship task/User Reviews.csv")

# Drop NaN values in the Rating column
apps_df = apps_df.dropna(subset=['Rating'])

# Fill missing values with mode for categorical data
apps_df.fillna(apps_df.mode().iloc[0], inplace=True)
apps_df.drop_duplicates(inplace=True)
apps_df = apps_df[apps_df['Rating'] <= 5]

# Clean Installs column
apps_df['Installs'] = apps_df['Installs'].str.replace(',', '').str.replace('+', '').astype(int)

# Clean Price column
apps_df['Price'] = apps_df['Price'].str.replace('$', '').astype(float)

# Merge DataFrames
merged_df = pd.merge(apps_df, reviews_df, on='App', how='inner')

# Convert Size column
def convert_Size(Size):
    if pd.isna(Size) or Size == 'Varies with device':
        return np.nan
    elif 'M' in Size:
        return float(Size.replace('M', ''))
    elif 'k' in Size:
        return float(Size.replace('k', '')) / 1024
    else:
        return np.nan

apps_df['Size'] = apps_df['Size'].apply(convert_Size)

# Log transformation
apps_df['Log_Installs'] = np.log1p(apps_df['Installs'])
apps_df['Reviews'] = apps_df['Reviews'].astype(int)

# Rating group classification
def rating_group(Rating):
    if Rating >= 4:
        return 'Top Rated'
    elif Rating >= 3:
        return 'Above Average'
    elif Rating >= 2:
        return 'Average'
    else:
        return 'Below Average'
    
apps_df['rating_group'] = apps_df['Rating'].apply(rating_group)

# Calculate revenue (fixing revenue calculation for free apps)
apps_df['Revenue'] = np.where(apps_df['Price'] == 0, 
                              apps_df['Installs'] * 0.01,  # Assuming $0.01 per install for free apps
                              apps_df['Installs'] * apps_df['Price'])

# Filtering conditions
filtered_df = apps_df[
    (apps_df['Installs'] >= 10000) &
    (apps_df['Revenue'] >= 10000) &
    (apps_df['Android Ver'].str.extract(r'(\d+\.\d+)').astype(float) > 4.0).squeeze() &
    (apps_df['Size'].fillna(0) > 15) &
    (apps_df['Content Rating'] == 'Everyone') &
    (apps_df['App'].str.len() <= 30)
]

# Get top 3 categories
top_categories = filtered_df['Category'].value_counts().nlargest(3).index
filtered_df = filtered_df[filtered_df['Category'].isin(top_categories)]

# Aggregate data using groupby
category_summary = filtered_df.groupby(['Category', 'Type']).agg({
    'Installs': 'mean',
    'Revenue': 'sum'
}).reset_index()

# Separate Free and Paid data
free_data = category_summary[category_summary["Type"] == "Free"]
paid_data = category_summary[category_summary["Type"] == "Paid"]

# Merge Free and Paid data correctly
merged_data = free_data.merge(
    paid_data, on="Category", suffixes=("_Free", "_Paid"), how="left"
)

# Visualization
fig2 = go.Figure()

# Add bar for Installs (Free) if available
if 'Installs_Free' in merged_data.columns:
    fig2.add_trace(go.Bar(
        x=merged_data['Category'],
        y=merged_data['Installs_Free'],
        name="Free Installs",
        marker_color='blue'
    ))

# Add bar for Installs (Paid) if available
if 'Installs_Paid' in merged_data.columns:
    fig2.add_trace(go.Bar(
        x=merged_data['Category'],
        y=merged_data['Installs_Paid'],
        name="Paid Installs",
        marker_color='green'
    ))

# Add line for Revenue (Free) if available
if 'Revenue_Free' in merged_data.columns:
    fig2.add_trace(go.Scatter(
        x=merged_data['Category'],
        y=merged_data['Revenue_Free'],
        name="Free Revenue",
        mode='lines+markers',
        yaxis="y2",
        line=dict(color='red', width=2)
    ))

# Add line for Revenue (Paid) if available
if 'Revenue_Paid' in merged_data.columns:
    fig2.add_trace(go.Scatter(
        x=merged_data['Category'],
        y=merged_data['Revenue_Paid'],
        name="Paid Revenue",
        mode='lines+markers',
        yaxis="y2",
        line=dict(color='orange', width=2)
    ))

# Update layout with correct dual-axis settings
fig2.update_layout(
    title="Comparison of Installs & Revenue (Free vs. Paid Apps)",
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    xaxis_title="Category",
    yaxis=dict(title="Average Installs"),
    yaxis2=dict(title="Total Revenue ($)", overlaying="y", side="right"),
    barmode="group",
    template="plotly_dark"
)    

ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
hour = current_time.hour

# Check time condition (1 PM - 2 PM IST)
if 13 <= hour < 14:
    fig2.write_html("task_2.html")
    print("Graph saved as task_2.html")
else:
    print("Graph is only available between 1 PM - 2 PM IST.")