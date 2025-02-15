import difflib

from spellchecker import SpellChecker


def spell_checker(word):
    """checks if the spelling is correct. used to make sure about OCR accuracy"""
    spell = SpellChecker()
    return spell.correction(word)


def most_similar_word(word, text):
    """
    finds the most similar word in the given text
    :param word: altered word
    :param text: text to be checked
    :return: the most similar word
    """
    words = text.split()
    return difflib.get_close_matches(word, words, n=1, cutoff=0.6)[0]  # Adjust cutoff if needed


def spell_correct(text: str) -> str:
    """
    reads the text and corrects the possible mistakes, returning the corrected text
    """
    for word in text.split():
        spell_corrected_word = spell_checker(word)
        if word != spell_corrected_word:
            text = text.replace(word, spell_corrected_word)

    return text
