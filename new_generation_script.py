import os
import sys
import json
from openai import OpenAI

def main(style_profile_path, prompt_text, output_file):
    # Load OpenAI API key from environment variable
    apikey = os.getenv('OPENAI_API_KEY')
    
    if not apikey:
        print("Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    client = OpenAI(api_key = apikey)
    # Load the writing style profile
    with open(style_profile_path, 'r', encoding='utf-8') as f:
        style_profile = json.load(f)

    # Construct the system prompt
    system_prompt = construct_system_prompt(style_profile)

    # Call the OpenAI API to generate text
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ],
        model="gpt-4o-mini",
    )

    generated_text = response.choices[0].message.content

    # Save the generated text to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(generated_text)

    print(f"Generated text has been saved to '{output_file}'.")

def construct_system_prompt(style_profile):
    # Extract features from the style profile
    avg_sentence_length = style_profile.get("average_sentence_length", 15)
    most_common_terms = style_profile.get("most_common_terms", [])
    most_common_bigrams = style_profile.get("most_common_bigrams", [])
    most_common_trigrams = style_profile.get("most_common_trigrams", [])
    avg_pos_proportions = style_profile.get("average_pos_proportions", {})
    avg_type_token_ratio = style_profile.get("average_type_token_ratio", 0.5)
    passive_voice_ratio = style_profile.get("passive_voice_ratio", 0.1)
    sentence_complexity_proportions = style_profile.get("sentence_complexity_proportions", {})
    average_sentiment = style_profile.get("average_sentiment", 0.0)
    average_readability = style_profile.get("average_readability", 8.0)
    punctuation_usage = style_profile.get("punctuation_usage", {})

    # Create a descriptive prompt that guides the model to match the writing style
    system_prompt = f"""
You are to generate text that matches the following writing style characteristics:

- **Average Sentence Length**: Aim for sentences averaging around {avg_sentence_length:.1f} words.
- **Lexical Choices**:
  - Use common terms such as: {', '.join([term for term, freq in most_common_terms[:10]])}.
  - Incorporate phrases like: {', '.join([phrase for phrase, freq in most_common_bigrams[:5]])}.
- **Vocabulary Diversity**: Maintain a type-token ratio of approximately {avg_type_token_ratio:.2f}, balancing common and unique words.
- **Part-of-Speech Usage**: Distribute parts of speech proportionally, focusing on these tags:
  {', '.join([f"{pos} ({freq*100:.1f}%)" for pos, freq in avg_pos_proportions.items() if freq > 0.05])}.
- **Sentence Complexity**: Include a mix of simple ({sentence_complexity_proportions.get('simple', 0)*100:.1f}%), compound ({sentence_complexity_proportions.get('compound', 0)*100:.1f}%), and complex ({sentence_complexity_proportions.get('complex', 0)*100:.1f}%) sentences.
- **Voice**: Use passive voice approximately {passive_voice_ratio*100:.1f}% of the time.
- **Sentiment**: Aim for an overall {'positive' if average_sentiment > 0 else 'negative' if average_sentiment < 0 else 'neutral'} tone.
- **Readability**: Write at a grade level of about {average_readability:.1f}.
- **Punctuation Usage**: Use punctuation marks proportionally, such as commas ({punctuation_usage.get(',', 0)*100:.1f}%), periods ({punctuation_usage.get('.', 0)*100:.1f}%).

Ensure the content is coherent and contextually appropriate for the user's prompt.
"""

    return system_prompt

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_text_with_style.py <style_profile.json> <output.txt>")
        sys.exit(1)

    style_profile_path = sys.argv[1]
    output_file = sys.argv[2]

    prompt_text = "Write a thriller story."

    main(style_profile_path, prompt_text, output_file)
