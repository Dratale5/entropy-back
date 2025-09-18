import math
from collections import Counter

class Entropy:
    @staticmethod
    def calculerEntropy(word: str) -> float:
        """
        Calculate the entropy of a given word.
        Entropy is calculated using the formula:
        H(X) = - Σ (p(x) * log2(p(x)))
        where p(x) is the probability of character x in the word.
        It will give a value between 1 and 5, where :
        - 1 : very weak (e.g., "aaaaaa")
        - 5 : very strong (e.g., "1¾÷6f%æ=Âæ:hßª©gzN")
        """
        if not word:
            return 0.0

        # Calculate frequency of each character in the word
        freq = {}
        for char in word:
            freq[char] = freq.get(char, 0) + 1

        # Calculate probabilities
        probabilities = [count / len(word) for count in freq.values()]

        # Calculate entropy
        entropy = -sum(p * math.log2(p) for p in probabilities)

        return entropy
    

    def calculerRedondance(texte):
        counts = Counter(texte)
        total = len(texte)
        N = len(counts)
        
        if N == 1:
            # If only 1 unique symbol, redundancy is maximal (1)
            return 1.0
        
        # Calculating entropy
        H = -sum((freq/total) * math.log2(freq/total) for freq in counts.values())
        
        # Calculating redundancy
        R = 1 - H / math.log2(N)
        
        return R

    