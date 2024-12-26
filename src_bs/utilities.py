import re
from collections import Counter

class Utilities:
    @staticmethod
    def get_word_counts(text_list):
        word_counts = Counter()
        for text in text_list:
            if text:
                words = re.findall(r'\b\w+\b', text.lower())
                word_counts.update(words)
        return word_counts
