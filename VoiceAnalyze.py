# This file is responsible for analyzing the text to find: Pace, Mood, Tone, and Voice

import os
import google.generativeai as genai # this will be done with Gemini
import sys # used for exiting when errors detected

os.environ['GOOGLE_API_KEY'] = "AIzaSyAnPPyK9rGs529uQ6pRZeiVcZ2a8IOg0HU" # for Gemini
genai.configure(api_key=os.environ['GOOGLE_API_KEY']) # for Gemini
model = genai.GenerativeModel("gemini-1.5-pro") # for Gemini

# provide the filepath where the user's example text is stored
# returns a the style features as a string
def analyzeVoice(self, filepath):
    useExampleText = ""
    try:
        with open(filepath, 'r') as file:
            useExampleText = file.read()
    except OSError as e: # FileNotFoundError is a sublcass of OSError
        print(f"Error opening user text file: {e}")
        sys.exit(1)

    try:
        analysisPrompt = f"Analyze the following text then return the following style features that describe the text: Pace, Mood, Tone, and Voice. Make sure to respond with only these style features.\n\n{useExampleText}"
        analysisResponse = model.generate_content(analysisPrompt)
        analysisResponse = analysisResponse.text
        return analysisResponse
    except Exception as e:
        print(f"Error with accessing Google Gemini: {e}")
        sys.exit(1)