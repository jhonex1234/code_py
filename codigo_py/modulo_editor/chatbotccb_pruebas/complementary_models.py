import re

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics.pairwise import cosine_similarity


class LengthTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [[len(x)] for x in X]

class DistanceClassifier:
    def __init__(self, patterns, labels, thresh=0.5):
        self._thresh = thresh
        self._patterns = patterns
        self._labels = labels if 'otro' in  labels else labels + ['otro']
        assert len(patterns) == len(labels), 'patterns y labels deberian tener igual longitud'

    @property
    def classes_(self):
        return self._labels

    def get_similarity(self, features):
        return cosine_similarity(features, self._patterns)

    def get_label(self, features):
        distances = self.get_similarity(features)
        return [self._labels[vector.argmax()] if vector.max() > self._thresh else 'otro'
                for vector in distances]

class RuleBasedClassifier(DistanceClassifier):
    def __init__(self, patterns, labels, thresh=0.5):
        super().__init__(patterns, labels, thresh)

    def get_similarity(self, samples):
        return np.array([[float(sample.lower().strip() == pattern) 
                          for pattern in self._patterns] for sample in samples])

    def get_label(self, samples):
        true_matrix = self.get_similarity(samples)
        return [self._labels[vector.argmax()] if vector.max() > self._thresh else 'otro'
                for vector in true_matrix]

class PatternFinder:
    def __init__(self, regex):
        self.__pattern = re.compile(regex)
        self.__ocurrence = []

    @property
    def ocurrence(self):
        return self.__ocurrence

    def get_pattern_occurrence(self, text):
        return self.__pattern.findall(text)

    def there_is_ocurrence(self, text):
        return bool(self.__occurrence(text))
