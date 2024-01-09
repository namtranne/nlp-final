from itertools import islice

import pkg_resources
from symspellpy import SymSpell, Verbosity

class ClosestPredictor:
    def __init__(self):
        self.sym_spell = SymSpell()
        self.dictionary_path = "/Users/tranhainam/anaconda3/lib/python3.11/site-packages/symspellpy/vietnamese_word_frequency.txt"
        self.bigram_path = "/Users/tranhainam/anaconda3/lib/python3.11/site-packages/symspellpy/vietnamese_bigram_frequency.txt"
        self.sym_spell.load_dictionary(self.dictionary_path, 0, 1)
        self.sym_spell.load_bigram_dictionary(self.bigram_path, term_index=0, count_index=2)

    def predict(self, input_term):
        suggestions = self.sym_spell.lookup(
            input_term, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=False
        )
        # Check if there are suggestions

        if suggestions:
            top_suggestion = suggestions[0].term
            return top_suggestion
        
        suggestions = self.sym_spell.lookup_compound(input_term, max_edit_distance=2)
        # display suggestion term, edit distance, and term frequency
        if suggestions:
            top_suggestion = suggestions[0].term
            return top_suggestion

        result = self.sym_spell.word_segmentation(input_term)
        return result.corrected_string

    def predict_long_word(self, input_tern):
        suggestions = self.sym_spell.lookup_compound(input_tern, max_edit_distance=2)
        # display suggestion term, edit distance, and term frequency
        if suggestions:
            top_suggestion = suggestions[0].term
            return top_suggestion

        result = self.sym_spell.word_segmentation(input_tern)
        return result.corrected_string