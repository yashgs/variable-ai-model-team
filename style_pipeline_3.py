import os
import sys
import json
import spacy
import nltk
from nltk.util import ngrams
from collections import Counter, defaultdict
import textstat
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer

def main(directory):
    nlp = spacy.load('en_core_web_sm')
    sia = SentimentIntensityAnalyzer()

    total_sentences = 0
    total_words = 0
    total_unique_words = set()
    num_files = 0

    type_token_ratios = []
    avg_sentence_lengths = []
    sentence_complexities = defaultdict(int)
    pos_counts_per_file = []
    term_frequencies = Counter()
    bigram_frequencies = Counter()
    trigram_frequencies = Counter()
    passive_sentence_count = 0
    total_sentiment = 0
    readability_scores = []
    punctuation_counts = Counter()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            num_files += 1
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                doc = nlp(text)

                # Readability Score
                readability = textstat.flesch_kincaid_grade(text)
                readability_scores.append(readability)

                # Sentiment Analysis
                sentiment = sia.polarity_scores(text)['compound']
                total_sentiment += sentiment

                # Sentences
                sentences = list(doc.sents)
                total_sentences += len(sentences)

                # Sentence lengths and complexities
                sentence_lengths = []
                for sent in sentences:
                    tokens = [token for token in sent if not token.is_punct and not token.is_space]
                    sentence_lengths.append(len(tokens))

                    # Detect passive voice
                    if any(token.dep_ == 'auxpass' for token in sent):
                        passive_sentence_count += 1

                    # Sentence Complexity
                    num_clauses = sum(1 for token in sent if token.dep_ == 'ccomp' or token.dep_ == 'advcl' or token.dep_ == 'relcl')
                    if num_clauses == 0:
                        sentence_complexities['simple'] += 1
                    elif num_clauses == 1:
                        sentence_complexities['compound'] += 1
                    else:
                        sentence_complexities['complex'] += 1

                if len(sentence_lengths) > 0:
                    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
                    avg_sentence_lengths.append(avg_sentence_length)
                else:
                    avg_sentence_lengths.append(0)

                # Words and POS tagging
                words_in_file = []
                pos_counts_file = Counter()
                for token in doc:
                    if not token.is_punct and not token.is_space:
                        total_words += 1
                        word = token.text.lower()
                        words_in_file.append(word)
                        pos_counts_file[token.pos_] += 1
                        term_frequencies[word] += 1
                        total_unique_words.add(word)

                        # Punctuation counts
                    elif token.is_punct:
                        punctuation_counts[token.text] += 1

                # Type-token ratio
                unique_words_in_file = set(words_in_file)
                type_token_ratio = len(unique_words_in_file) / len(words_in_file) if words_in_file else 0
                type_token_ratios.append(type_token_ratio)

                # POS proportions per file
                pos_counts_per_file.append(pos_counts_file)

                # N-grams
                bigrams = list(ngrams(words_in_file, 2))
                trigrams = list(ngrams(words_in_file, 3))
                bigram_frequencies.update(bigrams)
                trigram_frequencies.update(trigrams)

    if num_files == 0:
        print("No text files found in the specified directory.")
        sys.exit(1)

    # Average sentence length
    overall_avg_sentence_length = sum(avg_sentence_lengths) / len(avg_sentence_lengths)

    # Most common terms (normalized frequencies)
    total_word_count = total_words
    most_common_terms = [(term, count / total_word_count) for term, count in term_frequencies.most_common(20)]

    # Most common bigrams and trigrams
    total_bigrams = sum(bigram_frequencies.values())
    most_common_bigrams = [(" ".join(bigram), count / total_bigrams) for bigram, count in bigram_frequencies.most_common(20)]

    total_trigrams = sum(trigram_frequencies.values())
    most_common_trigrams = [(" ".join(trigram), count / total_trigrams) for trigram, count in trigram_frequencies.most_common(20)]

    # Average proportions of all parts of speech
    all_pos_tags = set()
    for pos_count in pos_counts_per_file:
        all_pos_tags.update(pos_count.keys())

    avg_pos_proportions = {pos: 0 for pos in all_pos_tags}
    for pos_count in pos_counts_per_file:
        total_pos = sum(pos_count.values())
        for pos in all_pos_tags:
            avg_pos_proportions[pos] += pos_count.get(pos, 0) / total_pos if total_pos > 0 else 0

    for pos in avg_pos_proportions:
        avg_pos_proportions[pos] /= len(pos_counts_per_file)

    # Average type-token ratio
    overall_avg_type_token_ratio = sum(type_token_ratios) / len(type_token_ratios)

    # Passive voice usage
    passive_voice_ratio = passive_sentence_count / total_sentences if total_sentences > 0 else 0

    # Sentence complexities proportions
    total_complexity_counts = sum(sentence_complexities.values())
    sentence_complexity_proportions = {key: count / total_complexity_counts for key, count in sentence_complexities.items()}

    # Average sentiment
    average_sentiment = total_sentiment / num_files

    # Average readability score
    average_readability = sum(readability_scores) / len(readability_scores)

    # Punctuation usage frequencies
    total_punctuations = sum(punctuation_counts.values())
    punctuation_usage = {punct: count / total_punctuations for punct, count in punctuation_counts.items()}

    # Writing style profile
    writing_style_profile = {
        "average_sentence_length": overall_avg_sentence_length,
        "most_common_terms": most_common_terms,
        "most_common_bigrams": most_common_bigrams,
        "most_common_trigrams": most_common_trigrams,
        "average_pos_proportions": avg_pos_proportions,
        "average_type_token_ratio": overall_avg_type_token_ratio,
        "passive_voice_ratio": passive_voice_ratio,
        "sentence_complexity_proportions": sentence_complexity_proportions,
        "average_sentiment": average_sentiment,
        "average_readability": average_readability,
        "punctuation_usage": punctuation_usage
    }

    with open('writing_style_profile.json', 'w', encoding='utf-8') as json_file:
        json.dump(writing_style_profile, json_file, ensure_ascii=False, indent=4)

    print("Writing style profile has been saved to 'writing_style_profile.json'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_of_text_files>")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)
