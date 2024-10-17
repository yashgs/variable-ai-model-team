import os
import google.generativeai as genai # for Gemini
import anthropic # for Claude

import sys # used for exiting when errors detected

os.environ['GOOGLE_API_KEY'] = "AIzaSyAnPPyK9rGs529uQ6pRZeiVcZ2a8IOg0HU" # for Gemini
genai.configure(api_key=os.environ['GOOGLE_API_KEY']) # for Gemini
model = genai.GenerativeModel("gemini-1.5-pro") # for Gemini

client = anthropic.Client(api_key=os.environ.get("ANTHROPIC_API_KEY", "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")) # for Claude

def uploadUserExampleTxt(self, userName="TODO", filepath="TODO"):
  # used for storing the user example text... filepath is the filepath of the user's text
  # userName will be the name of the user for storing their example text in a database
  # TODO!! Eventually, instead of uploading a txt file to colab we should be uploading it to a database
  print("This doesn't do anything")

def analyzeStyleFeatures(self, filepath, userName="TODO"):
  print("This doesn't do anything yet...")
  # TODO!! Do the actual style feature extraction here
  # Make sure to save the list of style features as a .txt file so that other methods can access the style features
  # Ultimately the style features will be saved into a database, but that won't be until we work with the full stack team

def getStyleFeatures(self, filepath, userName="TODO"):
    # uses userName to find the style features we have saved in the database for that user
    # (for now, we just save the style features as a .txt file)
    try:
      with open(filepath, 'r') as file:
        styleFeaturesString = file.read()
      return styleFeaturesString
    except OSError as e: # FileNotFoundError is a sublcass of OSError
      print(f"Error reading style features file: {e}")
      sys.exit(1)

def promptGemini(self, styleFeaturesString, userPrompt, styleTransferPrompt):
  # Since we want to be able to use 2 different models, it seemed cleaner to have a method for each model
  if not userPrompt:
      print("Error: userPrompt has not been provided. ")
      sys.exit(1)

  try:
        # get the basic response that DOESN'T consider style features
        preStyleTransferResponse = model.generate_content(userPrompt)
        preStyleTransferResponse = preStyleTransferResponse.text

        # Now performt he actual style transfer
        styleTransferPrompt = f"{styleTransferPrompt}\n\n{styleFeaturesString}\n\n{preStyleTransferResponse}"
        styleTransferResponse = model.generate_content(styleTransferPrompt)
        styleTransferResponse = styleTransferResponse.text
        return styleTransferResponse
  except Exception as e:
        print(f"Error with accessing Google Gemini: {e}")
        sys.exit(1)

def promptClaude(self, styleFeaturesString, userPrompt, styleTransferPrompt):
  try:
      # First, get the unmodified response to the user prompt
      preStyleTransferResponse = client.messages.create(
          model="claude-3-sonnet-20240229",
          max_tokens=1000,
          temperature=0.7,
          system="You are an AI assistant that fulfills user prompts.",
          messages=[
              {
                  "role": "user",
                  "content": userPrompt
              }
          ]
      )
      preStyleTransferResponse = preStyleTransferResponse.content[0].text

      # Second, perform the actual style transfer
      styleTransferPrompt = f"{styleTransferPrompt}\n\n{styleFeaturesString}\n\n{preStyleTransferResponse}"
      styleTransferResponse = client.messages.create(
          model="claude-3-sonnet-20240229",
          max_tokens=1000,
          temperature=0.7,
          system="You are an AI assistant that transforms text to match a given list of stylistic writing features.",
          messages=[
              {
                  "role": "user",
                  "content": styleTransferPrompt
              }
          ]
      )
      styleTransferResponse = styleTransferResponse.content[0].text
      return styleTransferResponse

  except Exception as e:
      return f"Error with accessing Claude: {e}"

def performPrompting(self, filepath, userPrompt, userName="TODO", modelType=1):
    # perform the actual prompting, then return the result
    # gets saved style features according to userName (this will be added later when we have a database)
    # when modelType=1 we use the free google gemini model, modelType=2 for paid Claude model (so that we can test this without spending money)

    # Eventually we will get the style features from a database. For now we just user filepath to represent where the style features .txt file is saved.
    styleFeaturesString = self.getStyleFeatures(filepath=filepath)

    # To tweak the prompt used, change this string
    styleTransferPrompt = "First I have listed multiple style features that describe someone's writing style. Use these features to apply them to the block of text in quotes that will follow the style features. Analyze the meaning of the block of text, then rewrite it so that it matches the style features listed. Respond with only the transformed text."

    if modelType == 1:
      # use google gemini
      return self.promptGemini(styleFeaturesString, userPrompt, styleTransferPrompt)
    elif modelType == 2:
      # Use Claude as the model
      return self.promptClaude(styleFeaturesString, userPrompt, styleTransferPrompt)
    else:
      print("Error: Invalid model argument (must be 1 for Gemini or 2 for Claude)")
      sys.exit(1)