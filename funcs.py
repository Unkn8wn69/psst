import os

# Conversion functions

def word_to_index(word, wordlist):
    try:
        return wordlist.index(word)
    except ValueError:
        raise ValueError(f"Word '{word}' not found in the wordlist.")

def index_to_word(index, wordlist):
    return wordlist[index]

def seed_to_hex(seed, wordlist):
    words = seed.split()
    indexes = [wordlist.index(word) for word in words]
    hex_string = ''.join(format(index, '03x') for index in indexes)
    return hex_string

def hex_to_seed(hex_string, wordlist):
    n = 3
    chunks = [hex_string[i:i+n] for i in range(0, len(hex_string), n)]
    seed = ' '.join(wordlist[int(chunk, 16)] for chunk in chunks)
    return seed

# Validation functions

def is_valid_seed(seed, wordlist):
    words = seed.split()
    valid_words = all(word in wordlist for word in words)
    valid_length = len(words) == 16
    return valid_words and valid_length

def validate_shares_and_threshold(num_shares, threshold):
    if num_shares > 16:
        print("The number of shares cannot exceed 16.")
        return False
    if threshold < 1 or threshold > num_shares:
        print("Threshold must be at least 1 and not more than the number of shares.")
        return False
    return True

# misc functions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')