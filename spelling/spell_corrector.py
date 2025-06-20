
from symspellpy.symspellpy import SymSpell, Verbosity
import os

# Initialize SymSpell object with max edit distance of 2
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load frequency dictionary (you must provide this file)
dictionary_path = "spelling/frequency_dictionary_en_82_765.txt"

if not os.path.exists(dictionary_path):
    raise FileNotFoundError("Please download 'frequency_dictionary_en_82_765.txt' from SymSpell repo.")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)


## Whitelist of common words to skip spell correction
whitelist = {"move", "circle", "line", "square", "pixels", "up", "down", "left", "right", "the", "to", "5", "10", "20"}

def spell_correct(text):
    words = text.split()
    corrected_words = []
    for word in words:
        if word in whitelist:
            corrected_words.append(word)
            continue
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            corrected_words.append(suggestions[0].term)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)