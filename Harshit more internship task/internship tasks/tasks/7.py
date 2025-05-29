import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load your dataset (replace the file path with the actual path to your CSV file)
df = pd.read_csv("C:/Users/venom/Desktop/internship task/Play Store Data.csv")  # Replace with your actual file path

# Inspect the first few rows to understand your dataset structure
print(df.head())

# Clean 'Reviews' column to handle non-numeric characters like 'M', 'K'
def clean_reviews(review):
    if isinstance(review, str):
        if 'M' in review:
            return float(review.replace('M', '')) * 1e6
        elif 'K' in review:
            return float(review.replace('K', '')) * 1e3
        else:
            return float(review)
    return review

# Apply the clean_reviews function to the 'Reviews' column
df['Reviews'] = df['Reviews'].apply(clean_reviews)

# Filter apps with name containing "C" and exclude apps with fewer than 10 reviews
filtered_data = df[df['App'].str.contains('C', case=False, na=False)]  # Filter app names containing 'C'
filtered_data = filtered_data[filtered_data['Reviews'] >= 10]  # Exclude apps with fewer than 10 reviews

# Filter apps with a rating less than 4.0
filtered_data = filtered_data[filtered_data['Rating'] < 4.0]

# Filter categories with more than 50 apps
category_counts = filtered_data['Category'].value_counts()
valid_categories = category_counts[category_counts > 50].index

# Filter the dataframe to include only the valid categories
filtered_data = filtered_data[filtered_data['Category'].isin(valid_categories)]

# Create the violin plot with Seaborn (matplotlib-based)
sns.violinplot(x='Category', y='Rating', data=filtered_data)  # Assuming 'Rating' is the column for app ratings

# Add labels and title (optional)
plt.title('Distribution of Ratings for Apps Containing "C", More Than 10 Reviews, and Rating < 4.0')
plt.xlabel('App Category')
plt.ylabel('Rating')

# Save the plot as an HTML file using Plotly
fig = px.violin(filtered_data, x='Category', y='Rating', box=True, points="all")
fig.update_layout(
    title='Distribution of Ratings for Apps Containing "C", More Than 10 Reviews, and Rating < 4.0',
    xaxis_title='App Category',
    yaxis_title='Rating'
)

# Save the figure as an HTML file
fig.write_html("C:/Users/venom/Desktop/task_7.html")  # Replace with your desired path

print("Plot saved as HTML successfully!")
