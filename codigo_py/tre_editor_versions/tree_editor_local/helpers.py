from collections import Counter
import json
import re
from unicodedata import normalize

from nltk.stem import SnowballStemmer
from sklearn.externals import joblib


class WordTokenizer:
    def __init__(self, remove_names=True, remove_greetings=True, remove_verbs=True, remove_additional=True):
        self.__tokenizer = re.compile(r'\b[a-zA-Z]{2,}\b')
        with open('unwanted_words.json', 'r') as file:
            unwanted_words = json.load(file)
        self.__stop_words = unwanted_words['commons']
        if remove_names:
            self.__stop_words += unwanted_words['names']
        if remove_greetings:
            self.__stop_words += unwanted_words['greetings']
        if remove_verbs:
            self.__stop_words += unwanted_words['verbs']
        if remove_additional:
            self.__stop_words += unwanted_words['additional']
        with open('spelling_dict.json', 'r') as file:
            self.__spelling_dict = json.load(file)
        self.__stemmer = SnowballStemmer('spanish').stem
        with open('exception_words.json', 'r') as file:
            self.__exception_words = json.load(file)

    def clear_text(self, text, normed=False, spell_checker=True, stemmed=True):
        """Tokeniza las palabras en text y realiza la limpieza"""
        if normed:
            text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode('utf-8') 
        words = self.__tokenizer.findall(text)        
        words = [word for word in words if word not in self.__stop_words and re.search('[aeiou]', word)
                 and re.search('[bcdfghjklmnpqrstvwxyz]', word)]
        if spell_checker:
            words = [self.__spelling_dict[word] if word in self.__spelling_dict else word 
                     for word in words]
        if stemmed:
            words = [self.__stemmer(word) if word not in self.__exception_words else word 
                     for word in words]
        return words

class SpellChecker:
    def __init__(self):
        # Diccionario de palabras.
        self.__words = joblib.load('words.pkl')        
        self.__num_words = float(sum(self.__words.values()))

    @property
    def num_words(self):
        return self.__num_words

    def edits2(self, word):
        """Todas las ediciones que sean dos ediciones de la palabra."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def edits1(self, word):
        """Todas las ediciones que sean una edicion de la palabra."""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def known(self, words, min_freq=1):
        """Subconjunto de ediciones que aparecen en el diccionario de palabras."""
        assert min_freq > 0, 'min_freq deberia ser mayor que 0'
        return set(w for w in words if self.__words[w] >= min_freq)

    def proba(self, word):
        """Probabilidad de la palabra."""
        return self.__words[word]/self.__num_words

    def correction(self, word, editions=1):
        """Retorna correccion ortografica mas probable para la palabra."""
        # Generar posibles correcciones ortograficas para la palabra.
        assert editions == 1 or editions == 2, 'editions deberia ser 1 o 2'
        candidates = (self.known([word]) | self.known(self.edits1(word)) | {word})
        if editions == 2:
            candidates |= self.known(self.edits2(word))
        return max(candidates, key=self.proba)
