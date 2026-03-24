import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

_vectorizer = TfidfVectorizer(max_features=512)
_svd = TruncatedSVD(n_components=128)
_fitted = False

def fit(corpus: list[str]):
    global _fitted
    if not corpus:
        return
    tfidf = _vectorizer.fit_transform(corpus)
    # n_components must be <= min(n_samples, n_features) - 1
    # Handle small corpuses during testing/seeding safely
    max_components = min(tfidf.shape[0], tfidf.shape[1]) - 1
    if max_components < 1:
        max_components = 1 # Fallback, though PCA won't do much

    actual_components = min(128, max_components)
    _svd.set_params(n_components=actual_components)

    _svd.fit(tfidf)
    _fitted = True

def embed(text: str) -> list[float]:
    if not _fitted:
        # Return a zero vector if not fitted (or raise, but zero is safer for initial DB insert)
        return [0.0] * 128

    tfidf = _vectorizer.transform([text])
    vec = _svd.transform(tfidf)[0]

    # Pad to 128 if SVD was forced to use fewer components due to tiny corpus
    if len(vec) < 128:
        vec = np.pad(vec, (0, 128 - len(vec)), 'constant')

    norm = np.linalg.norm(vec)
    return (vec / norm if norm > 0 else vec).tolist()
