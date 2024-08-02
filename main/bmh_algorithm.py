class BMHMatching:

    def __init__(self):
        self.text = ""
        self.bad_match_table = {}

    def set_text(self, text):
        self.text = text

    def __calculate_bad_match_table(self, pattern):
        patt_size = len(pattern)
        for i in range(patt_size - 1):
            self.bad_match_table[pattern[i]] = patt_size - i - 1

    def search(self, pattern):
        if not self.text or not pattern:
            return []

        text_size = len(self.text)
        patt_size = len(pattern)
        matches = []

        self.__calculate_bad_match_table(pattern)

        i = patt_size - 1
        while i < text_size:
            j = patt_size - 1
            k = i
            while j >= 0 and self.text[k] == pattern[j]:
                k -= 1
                j -= 1

            if j == -1:
                matches.append(k + 1)

            c = self.text[i]
            if c in self.bad_match_table:
                shift = self.bad_match_table[c]
            else:
                shift = patt_size
            i += shift

        return matches

    def search_first(self, pattern):
        if not self.text or not pattern:
            return []

        text_size = len(self.text)
        patt_size = len(pattern)
        matches = []

        self.__calculate_bad_match_table(pattern)

        i = patt_size - 1
        while i < text_size:
            j = patt_size - 1
            k = i
            while j >= 0 and self.text[k] == pattern[j]:
                k -= 1
                j -= 1

            if j == -1:
                return [(k + 1)]

            c = self.text[i]
            if c in self.bad_match_table:
                shift = self.bad_match_table[c]
            else:
                shift = patt_size
            i += shift

        return []
