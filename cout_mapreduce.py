import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Checking for HTTP errors
        return response.text
    except requests.RequestException as e:
        return None

# Function for deleting punctuation marks
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Execution MapReduce
def map_reduce(text, search_words=None):
    # Delete punctuation marks
    text = remove_punctuation(text)
    words = text.split()

    # If you specify a search word list, consider only these words
    if search_words:
        words = [word for word in words if word in search_words]

    # Parallel Mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Step 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Parallel Reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(result, top_n=10):
    top_words = Counter(result).most_common(top_n)

    # Split to words and counts
    words, counts = zip(*top_words)

    # Create graph
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequecy')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequet Words')
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == '__main__':
    # Input text for processing
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Executing MapReduce on input text
        result = map_reduce(text)

        visualize_top_words(result)
    else:
        print("Error: Could not get input.")