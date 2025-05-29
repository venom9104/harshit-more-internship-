import pandas as pd
import plotly.express as px

# Load dataset (update file path if needed)
df = pd.read_csv("C:/Users/venom/Desktop/internship task/Play Store Data.csv")
df = df[~df['Category'].str.startswith(('A', 'C', 'G', 'S'))]
# Convert 'Installs' column to numeric (removing commas and '+' signs)
df['Installs'] = df['Installs'].astype(str).str.replace(r'[+,]', '', regex=True)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# Group data by Category and sum the installs
category_installs = df.groupby('Category', as_index=False)['Installs'].sum()

# Select the top 5 categories by total installs
top_5_categories = category_installs.nlargest(5, 'Installs')

# Add a highlight column for categories with installs > 1 million
top_5_categories['Highlight'] = top_5_categories['Installs'].apply(lambda x: 'Highlighted' if x > 1_000_000 else 'Normal')

# Create Choropleth map
fig = px.choropleth(top_5_categories,
                    locations='Category',  
                    locationmode="ISO-3",  # Not using actual country codes, just for visualization
                    color='Installs',
                    hover_name='Category',
                    color_continuous_scale='Viridis',
                    title="Top 5 App Categories by Installs",
                    labels={'Installs': 'Total Installs'},
                    template="plotly_dark")

# Highlight categories with installs > 1M
for i, row in top_5_categories.iterrows():
    if row['Highlight'] == 'Highlighted':
        fig.add_annotation(
            x=row['Category'], 
            y=row['Installs'], 
            text="🔥 High Installs",
            showarrow=True,
            arrowhead=2,
            font=dict(color="red", size=12)
        )

# Show the plot
fig.show()

# Save the figure as an HTML file
fig.write_html("C:/Users/venom/Desktop/task_4.html")

print("Choropleth map saved successfully!")
