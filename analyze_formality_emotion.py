import os
import google.generativeai as genai  # Google Gemini integration
import sys  # Used for handling errors

# Set up your Google Gemini API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAnPPyK9rGs529uQ6pRZeiVcZ2a8IOg0HU"  # Replace with your actual API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])  # Configuring the Gemini API

# Define the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")  # Adjust model version as needed


# Function to analyze formality, emotion, and deeper stylistic features from a text file
def analyze_text(filepath):
    text_content = ""

    # Attempt to read the file and handle file-related errors
    try:
        with open(filepath, 'r') as file:
            text_content = file.read()
    except OSError as e:
        print(f"Error opening user text file: {e}")
        sys.exit(1)

    # Prepare the refined analysis prompt for Gemini
    try:
        analysis_prompt = (
            f"Analyze the following text and provide a detailed stylistic analysis, focusing on:\n"
            f"1. **Formality**: Is the writing formal, informal, or neutral?\n"
            f"2. **Emotion**: Describe the dominant emotions present in the text (e.g., happiness, sadness, anger, calmness, etc.). Also, rate the emotional intensity (high, medium, low).\n"
            f"Text:\n{text_content}"
        )

        # Generate content using the Gemini model
        analysis_response = model.generate_content(analysis_prompt)

        # Extract and return the analysis result
        analysis_result = analysis_response.text
        return analysis_result

    except Exception as e:
        print(f"Error accessing Google Gemini: {e}")
        sys.exit(1)


# Example usage
if __name__ == "__main__":
    filepath = "JoeyValenceLyrics.txt"  # Replace with the path to your text file
    result = analyze_text(filepath)
    print(f"Detailed Text Analysis:\n{result}")

