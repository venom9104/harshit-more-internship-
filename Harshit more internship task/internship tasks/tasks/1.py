import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download necessary NLTK data
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

# Load datasets
df = pd.read_csv(r"C:/Users/venom/Desktop/internship task/User Reviews.csv")
apps_df = pd.read_csv(r"C:/Users/venom/Desktop/internship task/Play Store Data.csv")

# Check and clean column names
df.columns = df.columns.str.strip()
apps_df.columns = apps_df.columns.str.strip()
print("Columns in User Reviews.csv:", df.columns)  # Debugging
print("Columns in Play Store Data.csv:", apps_df.columns)  # Debugging

# Ensure 'Rating' is numeric
apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')

# Convert app names to lowercase for better matching
app_name = set(apps_df['App'].dropna().str.lower())

def clean_text(Translated_Review):      
    if pd.isna(Translated_Review):
        return ""

    words = word_tokenize(str(Translated_Review))
    filtered_words = [word for word in words if word.lower() not in stopwords.words("english")]

    cleaned_text = " ".join(filtered_words)

    for app in app_name:
        cleaned_text = re.sub(rf"\b{re.escape(app)}\b", "", cleaned_text, flags=re.IGNORECASE)

    return cleaned_text.strip()

# Merge datasets to get 'Rating' in df
df = df.merge(apps_df[['App', 'Rating']], on='App', how='left')

# Filter reviews with Rating == 5
df_filtered = df[df["Rating"] == 4.9].copy()
print("Filtered data shape:", df_filtered.shape)
print("Filtered data sample:\n", df_filtered.head())

# Clean text in 'Translated_Review' column
df_filtered["cleaned_text"] = df_filtered["Translated_Review"].apply(clean_text)

# Save the filtered DataFrame
df_filtered.to_csv("filtered_data.csv", index=False)

print('Filtered data saved as filtered_data.csv')

# Generate Word Cloud from the cleaned reviews
all_reviews = " ".join(df_filtered["cleaned_text"])

# Create the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Save the word cloud image
wordcloud.to_file("wordcloud_5_star_reviews.png")

print("Word cloud generated and saved as 'wordcloud_5_star_reviews.png'.")
