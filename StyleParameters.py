import json
import os
import google.generativeai as genai

# Set your Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAnPPyK9rGs529uQ6pRZeiVcZ2a8IOg0HU"

# Configure the GenAI client
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load the Gemmini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Function to extract features
def extract_features(text):

    # Use the Gemmini model to generate a response based on the text
    response = model.generate_content( f"Analyze the text for figurative language, humor, diction, and rhetorical patterns: {text}")

    return response.text

# Read text file
with open("Writing_Sample.txt", "r") as f: #can be any text file here
    text = f.read()

# Extract features
features = extract_features(text)

# Save as JSON
with open("features.json", "w") as f:
    json.write(features, f)