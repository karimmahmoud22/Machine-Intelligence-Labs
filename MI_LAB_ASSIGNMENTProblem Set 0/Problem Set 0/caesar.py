from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

# Define a function to calculate the score of a deciphered text
def calculate_score(deciphered_text, dictionary_set):
    words = deciphered_text.split()
    # Count the number of words in the deciphered text that are not in the dictionary
    unknown_words = [word for word in words if word not in dictionary_set]
    return len(unknown_words)

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
    This function takes the ciphered text (string) and the dictionary (a list of strings where each string is a word).
    It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # Create a set from the dictionary for faster word lookup
    dictionary_set = set(dictionary)

    best_shift = 0
    # Set the minimum number of unknown words to infinity so that the first score will always be less than it
    min_unknown_words = float('inf')
    deciphered_text = ciphered

    # Iterate through all possible shifts
    for shift in range(26):
        decrypted_text = ''
        # Iterate through all characters in the ciphered text
        for char in ciphered:
            # If the character is a letter, shift it
            if char.isalpha():
                shifted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
                decrypted_text += shifted_char
            # If the character is not a letter, add it as is
            else:
                decrypted_text += char
        # Calculate the score of the decrypted text
        score = calculate_score(decrypted_text, dictionary_set)

        # If the score is better than the previous best score, update the best shift and the number of unknown words
        if score < min_unknown_words:
            best_shift = shift
            min_unknown_words = score
            deciphered_text = decrypted_text

    # Return the deciphered text, the best shift, and the number of unknown words
    return deciphered_text, best_shift, min_unknown_words
