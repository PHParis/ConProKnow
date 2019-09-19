from similarity.normalized_levenshtein import NormalizedLevenshtein


class Baseline(object):
    """Normalized Levenshtein https://pypi.org/project/strsim/#normalized-levenshtein"""

    def __init__(self):
        self.matcher = NormalizedLevenshtein()

    def similarity(self, seq1: str, seq2: str) -> float:
        return self.matcher.similarity(seq1, seq2)


if __name__ == "__main__":
    baseline = Baseline()
    print(baseline.similarity("jambon", "cornichon"))
    print(baseline.similarity("jambon", "jambon"))
    print(baseline.similarity("jambon", "janbon"))
