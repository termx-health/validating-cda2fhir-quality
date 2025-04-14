from sklearn.preprocessing import Binarizer
from sklearn.feature_extraction.text import CountVectorizer

class ValueTokensEmbedder():
    def __init__(self):
        self.vectorizer = CountVectorizer(
            token_pattern=r'(?u)\b\w+[-\.]\w+[-\.]\d+\b|\b[\w\-]+\b|[\d]+[,\.]\d+',
            lowercase=True
        )
        self.binarizer = Binarizer()

    def get_embeddings(self, values_sequences: list[str]) -> list[str]:
        # Transform sequences to count vectors
        count_vectors = self.vectorizer.fit_transform(values_sequences).toarray()
        # Convert to binary vectors while preserving concept map codes
        return self.binarizer.fit_transform(count_vectors)
