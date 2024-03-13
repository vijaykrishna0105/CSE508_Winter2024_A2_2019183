# -*- coding: utf-8 -*-
"""Copy of CSE508_Winter2024_A2_2019183.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iNwK07XbwpSGiStI_5NWaLEBL7hhBOoO
"""

from google.colab import drive
drive.mount('/content/drive')

save_directory = '/content/drive/MyDrive/IR_A2_files'

import os
import pandas as pd
import numpy as np

os.makedirs(save_directory, exist_ok=True)

# Adjust the path as necessary
dataset_path = '/content/drive/MyDrive/A2_Data.csv'
df = pd.read_csv(dataset_path)

# Display the first 5 rows of the dataframe to understand its structure
print(df.head())

from PIL import Image, ImageEnhance, ImageOps
import requests
from io import BytesIO
import numpy as np
import cv2

!pip install Pillow
!pip install requests

import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

# Assuming 'df' is your DataFrame
number_of_columns = len(df.columns)

print(f"Number of columns in the dataset: {number_of_columns}")

# Get the column names as a list
column_names = df.columns.tolist()

# Print the column names
print("Column names in the dataset:", column_names)

# Print the number of columns
print("Number of columns in the dataset:", len(column_names))

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def resize_image(image, size=(256, 256)):
    return image.resize(size)

def adjust_contrast(image, factor=2.0):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_brightness(image, factor=1.2):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def flip_image(image, direction='horizontal'):
    if direction == 'horizontal':
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        return image.transpose(Image.FLIP_TOP_BOTTOM)

def rotate_image(image, degrees=90):
    return image.rotate(degrees)

dataset_path = '/content/drive/MyDrive/A2_Data.csv'
df = pd.read_csv(dataset_path)

output_dir = '/content/drive/MyDrive/IR_A2_files'
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():
    # Assuming each cell in "Image" contains a single URL or a list of URLs as a string
    image_urls = eval(row['Image'])
    first_image_url = image_urls[0] if image_urls else None

    if first_image_url:
        try:
            # Load the image
            img = load_image_from_url(first_image_url)

            # Apply preprocessing steps
            img = resize_image(img)
            img = adjust_contrast(img)
            img = adjust_brightness(img)
            img = flip_image(img)
            img = rotate_image(img)

            # Save the processed image
            save_path = os.path.join(output_dir, f"processed_image_{row['Unnamed: 0']}.jpg")
            img.save(save_path)
        except Exception as e:
            print(f"Error processing image {first_image_url}: {e}")

print("Image processing complete.")

!pip install matplotlib

import requests
from PIL import Image, ImageEnhance
from io import BytesIO
import pandas as pd
import os
import matplotlib.pyplot as plt

# Your preprocessing functions as defined earlier

# Load the dataset
dataset_path = '/content/drive/MyDrive/A2_Data.csv'
df = pd.read_csv(dataset_path)

# Output directory
output_dir = '/content/drive/MyDrive/IR_A2_files'
os.makedirs(output_dir, exist_ok=True)

# Function to display images
def display_images(images, titles, nrows=1, ncols=2):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, nrows*5))
    for i, image in enumerate(images):
        ax[i].imshow(image)
        ax[i].set_title(titles[i])
        ax[i].axis('off')
    plt.show()

# Process and display the first 5 images
for index, row in df.head(5).iterrows():
    image_urls = eval(row['Image'])
    first_image_url = image_urls[0] if image_urls else None

    if first_image_url:
        try:
            # Load the image
            original_img = load_image_from_url(first_image_url)

            # Apply preprocessing steps
            processed_img = resize_image(original_img)
            processed_img = adjust_contrast(processed_img)
            processed_img = adjust_brightness(processed_img)
            processed_img = flip_image(processed_img)
            processed_img = rotate_image(processed_img)

            # Display before and after images
            display_images([original_img, processed_img], ['Before Processing', 'After Processing'])

            # Optionally save the processed image
            save_path = os.path.join(output_dir, f"processed_image_{row['Unnamed: 0']}.jpg")
            processed_img.save(save_path)
        except Exception as e:
            print(f"Error processing image {first_image_url}: {e}")

!pip install tensorflow

!pip install tensorflow pandas requests Pillow

from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

# Load the VGG16 model pre-trained on ImageNet data
model = VGG16(weights='imagenet', include_top=False)

# Display the model architecture
model.summary()

import requests
from PIL import Image
from io import BytesIO

def download_and_prepare_image(img_url, target_size=(224, 224)):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array_expanded_dims)

def extract_features_from_df(df, model):
    features_dict = {}
    for index, row in df.iterrows():
        image_urls = eval(row['Image'])  # Assuming this is a string representation of a list
        for img_url in image_urls:
            try:
                preprocessed_image = download_and_prepare_image(img_url)
                features = model.predict(preprocessed_image)
                features_dict[img_url] = features
            except Exception as e:
                print(f"Error processing image URL {img_url}: {e}")
    return features_dict

image_features = extract_features_from_df(df, model)

import pickle

# Define the path where you want to save the image features
features_file_path = '/content/drive/MyDrive/IR_A2_files/image_features.pkl'

# Save the image_features dictionary to a file
with open(features_file_path, 'wb') as file:
    pickle.dump(image_features, file)

import numpy as np

def l2_normalize(features):
    """
    Apply L2 normalization to a set of features.
    Args:
    - features (numpy.ndarray): The feature array to normalize, shape (n_samples, n_features)

    Returns:
    - normalized_features (numpy.ndarray): L2 normalized feature array.
    """
    norm = np.linalg.norm(features, axis=1, keepdims=True)
    normalized_features = features / norm
    return normalized_features

# Assuming image_features is a dictionary with URLs as keys and features as values
normalized_image_features = {}
for url, features in image_features.items():
    # features.squeeze() to convert (1, 7, 7, 512) to (7, 7, 512) for VGG16 example
    # You may need to adjust the reshaping based on the specific output of your model
    flattened_features = features.squeeze().reshape(-1)
    normalized_features = l2_normalize(flattened_features[np.newaxis, :])  # np.newaxis to add batch dimension
    normalized_image_features[url] = normalized_features

# Now, normalized_image_features contains the L2 normalized features for each image

def show_normalization_effect(image_features, normalized_image_features):
    urls = list(image_features.keys())[:5]  # Get the first 5 URLs

    for url in urls:
        original_features = image_features[url].squeeze()  # Assuming features are stored in a numpy array
        normalized_features = normalized_image_features[url].squeeze()

        # Compute the L2 norm of the original and normalized features
        original_norm = np.linalg.norm(original_features)
        normalized_norm = np.linalg.norm(normalized_features)

        print(f"URL: {url}")
        print(f"Original L2 Norm: {original_norm}")
        print(f"Normalized L2 Norm: {normalized_norm}")
        print("-" * 30)

# Assuming you've followed the previous steps to extract and normalize features
show_normalization_effect(image_features, normalized_image_features)

from IPython.display import Image, display

urls = [
    "https://images-na.ssl-images-amazon.com/images/I/81q5+IxFVUL._SY88.jpg",
    "https://images-na.ssl-images-amazon.com/images/I/71HSx4Y-5dL._SY88.jpg",
    "https://images-na.ssl-images-amazon.com/images/I/71dVsYejzTL._SY88.jpg",
    "https://images-na.ssl-images-amazon.com/images/I/71domStNfIL._SY88.jpg",
    "https://images-na.ssl-images-amazon.com/images/I/71Md5ihUFLL._SY88.jpg"
]

for url in urls:
    display(Image(url=url))

!pip install tensorflow

import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
import requests
from io import BytesIO
from sklearn.preprocessing import StandardScaler



!pip install nltk scikit-learn

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

"""# **Text Feature Extraction(recheck)**"""

!pip install nltk

import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Check if the text is a string
    if not isinstance(text, str):
        return ""  # or return some placeholder text like "missing"

    # Proceed with preprocessing if it's a string
    text = text.lower()  # Lower-casing
    text = re.sub(r'[^\w\s]', '', text)  # Removing punctuation
    tokens = word_tokenize(text)  # Tokenization

    # Stop Word Removal
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(tokens)



    return ' '.join(tokens)

review_texts = [
    "Loving these vintage springs on my vintage strat. They have a great vibe.",
    "Works great as a guitar bench mat. Not rugged but fine for home use.",
    "We use these for everything from our acoustic gigs to full on rock shows. Very versatile.",
    "Great price and good quality. It didn't quite fit my model but with minor adjustments it worked well.",
    "I bought this bass to split time as my primary. It has become my go-to for everything."
]


preprocessed_texts = [preprocess_text(text) for text in review_texts]

# Display before and after preprocessing
for original, preprocessed in zip(review_texts, preprocessed_texts):
    print(f"Original: {original}\nPreprocessed: {preprocessed}\n" + "-"*75)

# Assuming 'df' is your DataFrame and it has a column named 'Review Text'
df['Processed Review Text'] = df['Review Text'].apply(preprocess_text)

# Count the number of non-empty (non-null) entries in the 'Processed Review Text' column
# num_processed = df['Processed Review Text'].apply(bool).sum()

# print(f"Number of processed texts: {num_processed}")

# Defining  the output path
output_path = '/content/drive/MyDrive/IR_A2_files/processed_reviews.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the DataFrame with processed review texts to a new CSV file
df.to_csv(output_path, index=False)

print("Preprocessed texts have been saved.")

!pip install scikit-learn

from sklearn.feature_extraction.text import TfidfVectorizer

# Assuming 'df' is your DataFrame and it contains a column 'Processed Review Text'
# with preprocessed text reviews

# Initialize a TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the preprocessed reviews to calculate TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Processed Review Text'])

# tfidf_matrix now contains the TF-IDF scores with one row per document (review)
# and one column per word (feature)
# Convert the TF-IDF matrix into a DataFrame for better readability
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
# If you want to see the vocabulary (mapping of word to feature index)
vocabulary = tfidf_vectorizer.get_feature_names_out()

# Example: Print the TF-IDF scores for the first document
first_document_tfidf = tfidf_matrix[0].toarray()
print("TF-IDF scores for the first document:")
print(dict(zip(vocabulary, first_document_tfidf[0])))

# To get a sense of the dimensionality
print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

# Sample textual reviews
reviews = [
    "This product is great, I liked it",
    "I hated this product, it was terrible",
    "Best purchase ever, this product is amazing",
    "Not what I expected, but the product is okay",
    "I have mixed feelings about this product"
]

# Import required libraries
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Initialize a TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the reviews to a TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(reviews)

# Convert the TF-IDF matrix to a DataFrame for better readability
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Display the DataFrame
print(tfidf_df)

# Save the entire TF-IDF DataFrame to a CSV file
tfidf_df.to_csv('tfidf_scores.csv', index=False)

import os
import json

# Create a directory for the individual TF-IDF score files
os.makedirs('tfidf_scores', exist_ok=True)

# Iterate through the DataFrame and save each review's TF-IDF scores as a separate JSON file
for index, row in tfidf_df.iterrows():
    # Convert the row to a dictionary
    tfidf_dict = row.to_dict()
    # Define a filename based on the review index
    filename = f'tfidf_scores/review_{index+1}.json'
    # Save the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(tfidf_dict, file)

"""# **Image Retrieval and Text Retrieval(Recheck)**"""

import pandas as pd
from PIL import Image as PILImage
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, ResNet50
from tensorflow.keras.models import Model

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_cosine_similarity(feature1, feature2):
    # Ensure the features are in the right shape and dtype
    feature1 = np.array(feature1).reshape(1, -1)
    feature2 = np.array(feature2).reshape(1, -1)

    # Calculate and return the cosine similarity
    return cosine_similarity(feature1, feature2)[0][0]

def find_most_similar_images(input_img_url, image_features, top_n=3):
    # First, extract features for the input image
    input_features = image_features.get(input_img_url)
    if input_features is None:
        raise ValueError("The input image URL is not found in the dataset.")

    similarities = []

    # Calculate similarity of input image with all other images
    for url, features in image_features.items():
        similarity = calculate_cosine_similarity(input_features, features)
        similarities.append((url, similarity))

    # Sort based on similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return top N similar image URLs, excluding the input image itself
    return [url for url, sim in similarities[:top_n + 1] if url != input_img_url][:top_n]

import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity

# Simulate loading your dataset (replace this with your actual dataset loading)
df = pd.DataFrame({
    'Image': [
        "['https://images-na.ssl-images-amazon.com/images/I/81%2B5JiB1qSL._AC_SL1500_.jpg']",
        "['https://images-na.ssl-images-amazon.com/images/I/71%2B5JiB1qSL._AC_SL1500_.jpg']",
        "['https://images-na.ssl-images-amazon.com/images/I/61%2B5JiB1qSL._AC_SL1500_.jpg']"
    ]
})

# Simulate feature extraction for 3 images (you would use your actual feature extraction method here)
features = {
    "Image1": np.array([0.8, 0.1, 0.1]),
    "Image2": np.array([0.7, 0.2, 0.1]),
    "Image3": np.array([0.1, 0.9, 0.0]),
}

# Select a random image as input
input_image_url = random.choice(df['Image'].tolist())
input_image_key = "Image" + str(random.randint(1, 3))  # Simulate selecting a corresponding feature vector

# Calculate cosine similarity between the input image and others
similarity_scores = {}
for img, feat in features.items():
    if img != input_image_key:  # Exclude the input image itself
        similarity = cosine_similarity(features[input_image_key].reshape(1, -1), feat.reshape(1, -1))[0][0]
        similarity_scores[img] = similarity

# Sort the images by similarity score, highest first
most_similar_images = sorted(similarity_scores, key=similarity_scores.get, reverse=True)

print(f"Input Image: {input_image_url}")
print("Most similar images in order:", most_similar_images)

def find_similar_images(user_input_url):
    # Simulate finding the corresponding feature vector for the user input URL
    # In a real application, this should directly look up the feature vector for the provided URL
    input_image_key = None
    for key, url in df['Image'].iteritems():
        if user_input_url in url:
            input_image_key = "Image" + str(key + 1)  # Adjust based on your actual mapping
            break

    # Handle case where the URL is not found
    if input_image_key is None or input_image_key not in features:
        print("Input URL not found in the dataset.")
        return

    # Calculate cosine similarity between the input image and others
    similarity_scores = {}
    for img, feat in features.items():
        if img != input_image_key:  # Exclude the input image itself
            similarity = cosine_similarity(features[input_image_key].reshape(1, -1), feat.reshape(1, -1))[0][0]
            similarity_scores[img] = similarity

    # Sort the images by similarity score, highest first
    most_similar_images = sorted(similarity_scores, key=similarity_scores.get, reverse=True)

    print(f"Input Image: {user_input_url}")
    print("Most similar images in order:", most_similar_images)

# Example usage:
user_input_url = "https://images-na.ssl-images-amazon.com/images/I/81%2B5JiB1qSL._AC_SL1500_.jpg"  # User input
find_similar_images(user_input_url)

import random

# Calculate the sample size as the minimum of 5 or the number of rows in the DataFrame
sample_size = min(5, len(df))

# Use the calculated sample size to sample the DataFrame
random_image_urls = df['Image'].sample(n=sample_size).tolist()

# Sort pairs by similarity score
sorted_pairs = sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)

# Display the most similar pair(s)
for pair, score in sorted_pairs[:3]:  # Let's display the top 3 pairs
    print(f"Pair: {pair}, Similarity Score: {score}")

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the DataFrame with processed review texts
df = pd.read_csv('/content/drive/MyDrive/IR_A2_files/processed_reviews.csv')

# Fill missing values with empty strings
df['Processed Review Text'] = df['Processed Review Text'].fillna('')

# Now, proceed with TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Processed Review Text'])

# The rest of your code for finding similar reviews can follow here


# Select an input review index (e.g., using the first review as input)
input_review_index = 1  # Adjust as needed or select randomly
input_tfidf_vector = tfidf_matrix[input_review_index]

# Calculate Cosine Similarity between the input review and all other reviews
cosine_similarities = cosine_similarity(input_tfidf_vector, tfidf_matrix).flatten()

# Find indices of the top 3 most similar reviews, excluding the input review itself
# Note: argsort()[::-1] sorts indices by descending similarity, excluding the first one
similar_indices = cosine_similarities.argsort()[-4:-1][::-1]  # Excludes the highest score (itself)

# Print the most similar reviews and their scores
print("Most similar reviews based on TF-IDF and Cosine Similarity:")
for index in similar_indices:
    # Adjust print statement as necessary to include any additional details
    print(f"Review {index + 1}: {df['Processed Review Text'].iloc[index]} (Score: {cosine_similarities[index]})")

def find_similar_reviews(user_input_text):
    # Ensure the input is in a list format as expected by the vectorizer
    user_input_tfidf_vector = tfidf_vectorizer.transform([user_input_text])

    # Calculate Cosine Similarity
    cosine_similarities = cosine_similarity(user_input_tfidf_vector, tfidf_matrix).flatten()

    # Find indices of the top 3 most similar reviews
    similar_indices = cosine_similarities.argsort()[-3:][::-1]  # Gets top 3 indices

    # Print the most similar reviews and their scores
    print("Most similar reviews based on TF-IDF and Cosine Similarity:")
    for index in similar_indices:
        print(f"Review {index + 1}: {df['Processed Review Text'].iloc[index]} (Score: {cosine_similarities[index]})")

# Example user input
user_input_text = "Enter your review text here"  # Replace this with actual user input
find_similar_reviews(user_input_text)

import pickle

# Assuming tfidf_matrix is the TF-IDF matrix you want to save
# You can replace 'tfidf_matrix' with any other Python object you wish to save
output_path = '/content/drive/MyDrive/IR_A2_files/tfidf_matrix.pkl'

# Saving the TF-IDF matrix to a file
with open(output_path, 'wb') as file:
    pickle.dump(tfidf_matrix, file)

print("TF-IDF matrix has been saved to", output_path)

import pickle

# The path to the file containing the saved TF-IDF matrix
input_path = '/content/drive/MyDrive/IR_A2_files/tfidf_matrix.pkl'

# Loading the TF-IDF matrix from the file
with open(input_path, 'rb') as file:
    tfidf_matrix_loaded = pickle.load(file)

print("TF-IDF matrix has been loaded.")

# Assuming cosine_similarities is the array of cosine similarity scores you want to save
cosine_similarities_path = '/content/drive/MyDrive/IR_A2_files/cosine_similarities.pkl'

# Saving the cosine similarity scores to a file
with open(cosine_similarities_path, 'wb') as file:
    pickle.dump(cosine_similarities, file)

print("Cosine similarity scores have been saved.")

# Loading the cosine similarity scores from the file
with open(cosine_similarities_path, 'rb') as file:
    cosine_similarities_loaded = pickle.load(file)

print("Cosine similarity scores have been loaded.")

import pandas as pd

# Assuming tfidf_matrix_loaded is the loaded TF-IDF matrix
# Convert the first 5 rows of the TF-IDF matrix to a DataFrame for easy viewing
tfidf_matrix_df = pd.DataFrame(tfidf_matrix_loaded[:5].toarray())

print("First 5 rows of the loaded TF-IDF matrix:")
print(tfidf_matrix_df)

# Assuming cosine_similarities_loaded contains the loaded cosine similarity scores
# Display the first 5 cosine similarity scores
print("First 5 cosine similarity scores:")
print(cosine_similarities_loaded[:5])

"""# **Combined Retrieval(Recheck)**"""



"""# **Combined Retrieval**"""

# # Assuming image_similarity_scores and text_similarity_scores are lists or arrays of the same length
# composite_scores = [(img_score + txt_score) / 2 for img_score, txt_score in zip(image_similarity_scores, text_similarity_scores)]

# # Rank the pairs based on composite score
# # If you need to keep track of the original indices/pairs, consider using enumerate and sorting by score
# ranked_pairs_indices = sorted(range(len(composite_scores)), key=lambda i: composite_scores[i], reverse=True)

# # Now ranked_pairs_indices contains indices sorted by the highest composite score
# # Use these indices to retrieve or reference the original pairs

# # Example: Print top 3 ranked pairs
# print("Top 3 ranked pairs based on composite similarity score:")
# for idx in ranked_pairs_indices[:3]:
#     print(f"Pair {idx} with composite score: {composite_scores[idx]}")

# Recalculate the image similarity for demonstration
# Choose an input image features vector
input_image_features = features_array[0].reshape(1, -1)  # Example: Taking the first image's features

# Calculate cosine similarity for images
image_similarity_scores = cosine_similarity(input_image_features, features_array)[0]

# Assuming you have an input review's TF-IDF vector
# This would have been generated similar to how you processed all reviews into the tfidf_matrix
# For demonstration, let's assume it's the TF-IDF vector for the first review
input_review_vector = tfidf_matrix[0:1]

# Calculate cosine similarity for text
text_similarity_scores = cosine_similarity(input_review_vector, tfidf_matrix).flatten()

# Calculate composite scores by averaging image and text similarity scores
composite_scores = [(img_score + txt_score) / 2 for img_score, txt_score in zip(image_similarity_scores, text_similarity_scores)]

# Rank the pairs based on composite score
ranked_pairs_indices = sorted(range(len(composite_scores)), key=lambda i: composite_scores[i], reverse=True)

# Example: Print top 3 ranked pairs based on composite similarity score
print("Top 3 ranked pairs based on composite similarity score:")
for idx in ranked_pairs_indices[:3]:
    print(f"Pair {idx} with composite score: {composite_scores[idx]}")

from IPython.display import display, Image
import ast

# Function to display an image from a URL
def display_image_from_url(url):
    display(Image(url=url))

# Assuming `df` is your DataFrame
for idx in [0, 67, 271]:  # Example indices from your results
    print(f"Pair {idx} with composite score: {composite_scores[idx]}")
    row = df.iloc[idx]
    image_urls = ast.literal_eval(row['Image'])
    if image_urls:
        print("Displaying Image:")
        display_image_from_url(image_urls[0])
    print("Review:", row['Review Text'])
    print("\n---\n")

# Calculate composite similarity scores as the average of image and text similarity scores
composite_similarity_scores = [(img_score + text_score) / 2 for img_score, text_score in zip(image_similarity_scores, text_similarity_scores)]

# Example scores for demonstration; replace these with your actual similarity scores
# image_similarity_scores = [0.8, 0.5, 0.9]  # Example data
# text_similarity_scores = [0.7, 0.6, 0.4]   # Example data

# Calculate composite similarity scores as the average of image and text similarity scores
composite_similarity_scores = [(img_score + text_score) / 2 for img_score, text_score in zip(image_similarity_scores, text_similarity_scores)]

# Sort the indices of these scores in descending order to rank them from most to least similar
sorted_indices = sorted(range(len(composite_similarity_scores)), key=lambda i: composite_similarity_scores[i], reverse=True)

# Now, use sorted_indices to get the top N similar pairs
top_n = 3  # Adjust based on how many top pairs you'd like to retrieve
top_n_indices = sorted_indices[:top_n]

print(f"Top {top_n} similar pairs (based on composite similarity score):")
for idx in top_n_indices:
    print(f"Pair {idx} with composite score: {composite_similarity_scores[idx]}")
    # Optionally, display or process the corresponding image and text pair as needed

"""# **Results & Analysis**"""

from IPython.display import display, Image
import ast

# Function to display an image from a URL
def display_image_from_url(url):
    display(Image(url=url))

# Display top-ranked pairs
for idx in [0, 67, 271]:
    # Assuming you have a dataframe `df` with 'Image' and 'Review Text' columns
    image_urls = ast.literal_eval(df.iloc[idx]['Image'])
    review_text = df.iloc[idx]['Review Text']
    composite_score = composite_similarity_scores[idx]

    print(f"Pair {idx} with composite score: {composite_score}")
    if image_urls:  # Check if there are any image URLs
        display_image_from_url(image_urls[0])  # Display the first image
    print("Review:", review_text)
    print("\n---\n")

"""# **Sample Test Cases**"""

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from PIL import Image
import requests
from io import BytesIO

# Initialize the pre-trained model
base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)

def download_and_process_img(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).resize((224, 224))
    img_array = img_to_array(img)
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array_expanded)

def extract_features(processed_img):
    return model.predict(processed_img)

# Assuming the following functions are defined and models are loaded:
# - download_and_process_img(img_url) -> processes the image for the model
# - extract_features(image) -> returns the feature vector for an image
# - tfidf_vectorizer -> TF-IDF vectorizer fitted on your dataset
# - image_similarity_scores, text_similarity_scores -> arrays/lists containing pre-calculated scores

# Input
input_img_url = "https://images-na.ssl-images-amazon.com/images/I/71bztfqdg+L._SY88.jpg"
input_review_text = "I have been using Fender locking tuners for about five years on various strats and teles. Definitely helps with tuning stability and way faster to restring if there is a break."

# Process the input image and text
input_img_processed = download_and_process_img(input_img_url)
input_img_features = extract_features(input_img_processed).flatten()
input_text_vector = tfidf_vectorizer.transform([input_review_text])

# Calculate similarities
image_similarity_scores = cosine_similarity(input_img_features.reshape(1, -1), features_array)
text_similarity_scores = cosine_similarity(input_text_vector, tfidf_matrix)

# Combine and rank (simplified version, real implementation will depend on your data structures)
composite_scores = [(img_score + txt_score) / 2 for img_score, txt_score in zip(image_similarity_scores.flatten(), text_similarity_scores.flatten())]
sorted_indices = sorted(range(len(composite_scores)), key=lambda i: composite_scores[i], reverse=True)

# Output for top 3
for idx in sorted_indices[:3]:
    print(f"{idx+1}) Image URL: {df.iloc[idx]['Image']}")
    print(f"Review: {df.iloc[idx]['Review Text']}")
    print(f"Cosine similarity of images - {image_similarity_scores[0][idx]:.4f}")
    print(f"Cosine similarity of text - {text_similarity_scores[0][idx]:.4f}")
    print("---")

# Composite Scores (example, adjust according to how you calculate/store these)
print(f"Composite similarity scores of images: {np.mean(image_similarity_scores):.4f}")
print(f"Composite similarity scores of text: {np.mean(text_similarity_scores):.4f}")
final_composite_score = np.mean(composite_scores)
print(f"Final composite similarity score: {final_composite_score:.4f}")