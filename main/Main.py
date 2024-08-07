from bmh_algorithm import BMHMatching
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class RegEx:
    def __init__(self):
        self.text = ""
        self.original_text = ""
        self.fr = False  # False = Search only, True = Search and Replace
        self.g = False  # False = First match only, True = All matches
        self.i = False  # False = Case sensitive, True = Case insensitive
        self.replacement = ""
        self.file = None
        self.searcher = BMHMatching()  # BMH

    def main(self, file):
        self.set_text(file)
        self.original_text = self.text

        root = tk.Tk()
        root.geometry('1000x600')
        root.configure(background="gray")
        root.title("RegEx replica")
        root.resizable(False, False)

        # Recover original file
        def restore_original_content():
            if self.original_text and self.file:
                with open(self.file, 'w') as archivo:
                    archivo.write(self.original_text)

            print("Original content restored")
            root.destroy()

        # Find and underline occurrences
        def search():
            query = entry.get()
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", self.text)
            text_widget.tag_remove("highlight", "1.0", tk.END)

            if not query:
                messagebox.showinfo("Error", "Empty, enter a query.")
                return

            pattern = self.compute_query(query)  # Extract pattern from query and assign options
            occurrences = self.search(pattern)  # Search occurrences of the pattern in the text
            occurrences.sort()
            print(occurrences)

            text_widget.tag_configure("highlight", background="light blue")

            if self.fr:  # In the case of find and replace, it does not underline the occurrences.
                text_widget.config(state='normal')
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", self.text)
                text_widget.tag_remove("highlight", "1.0", tk.END)
                text_widget.config(state="disabled")

                # Shows the number of occurrences
                occ_num = "Occurrences: " + str(len(occurrences))
                label2.config(text=occ_num)
            else:
                if '|' in pattern:  # If you have an OR, calculate the occurrences of each pattern
                    tokens = pattern.split()
                    occurrences1 = self.search(tokens[0])
                    for index in occurrences1:
                        start = f"1.0 + {index} chars"
                        end = f"{start} + {self.get_patt_size(tokens[0])} chars"
                        text_widget.tag_add("highlight", start, end)

                    occurrences2 = self.search(tokens[2])
                    for index in occurrences2:
                        start = f"1.0 + {index} chars"
                        end = f"{start} + {self.get_patt_size(tokens[2])} chars"
                        text_widget.tag_add("highlight", start, end)

                else:  # For any other type of search
                    for index in occurrences:
                        start = f"1.0 + {index} chars"
                        end = f"{start} + {self.get_patt_size(pattern)} chars"
                        text_widget.tag_add("highlight", start, end)

                # Shows the number of occurrences
                occ_num = "Occurrences: " + str(len(occurrences))
                label2.config(text=occ_num)

                text_widget.config(state="disabled")

        left_frame = tk.Frame(root, background='#CCCCCC')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(root, width=600, background='#CCCCCC')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)

        label1 = ttk.Label(left_frame, text="Modified RegEx", font=("Arial", 24), background='#CCCCCC')
        label1.pack(pady=20)

        entry = ttk.Entry(left_frame, width=20, font=("Arial", 14))
        entry.pack(pady=10)

        style = ttk.Style()
        style.configure("Custom.TButton", font=("Arial", 14), background="gray", foreground="black", relief="flat",
                        width=11, height=2)
        button = ttk.Button(left_frame, text="Search", style="Custom.TButton", command=search)
        button.pack(pady=0)

        label2 = ttk.Label(left_frame, text="Occurrences:", font=("Arial", 14), background='#CCCCCC')
        label2.pack(pady=20)

        max_text_width = 400
        text_widget = tk.Text(right_frame, font=("Arial", 16), state='normal', width=max_text_width // 10)
        text_widget.insert("1.0", self.text)
        text_widget.config(state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        root.protocol("WM_DELETE_WINDOW", restore_original_content)

        root.mainloop()

    # Read a file and assign it as the text to use
    def set_text(self, file):
        self.file = file
        with open(file, 'r') as arch:
            self.text = arch.read()

    # Get the actual length of a pattern
    def get_patt_size(self, pattern):
        # Simple patterns, no changes required
        if not any(char in pattern for char in ['[', '-', '*', '?', '|', '{']):
            return len(pattern)

        # Patterns with range, range counts as a single character
        if '[' in pattern and ']' in pattern and '-' in pattern:
            index_start = pattern.find('[') + 1
            index_end = pattern.find(']') - 1
            pattern_other = pattern[:index_start - 1] + pattern[index_end + 2:]
            length = len(pattern_other) + 1
            return length

        # Patterns with character set, the set counts as a single character
        if '[' in pattern and ']' in pattern and '-' not in pattern:
            index_start = pattern.find('[') + 1
            index_end = pattern.find(']') - 1
            pattern_other = pattern[:index_start - 1] + pattern[index_end + 2:]
            length = len(pattern_other) + 1
            return length

        # # Wildcard patterns, no changes required
        if '*' in pattern:
            return len(pattern)

        # Patterns with '?', count the pattern without the symbol
        if '?' in pattern:
            return len(pattern) - 2

        # Patterns with repetition, builds the pattern with the repeated character
        if '{' in pattern:
            index = pattern.find('{')
            repetitions = int(pattern[index + 1])
            pattern_other = pattern[:index - 1] + (pattern[index - 1] * repetitions) + pattern[index + 3:]
            return len(pattern_other)

    # Function to interpret the query, assign corresponding values ​​and extract the pattern
    def compute_query(self, query):
        tokens = query.split()
        pattern = ""

        if tokens[0] == 'fr':  # Search and replace
            self.fr = True
            pattern = tokens[1]
            self.replacement = tokens[2]

            if len(tokens) > 2 and tokens[2] == '|':
                pattern += " " + tokens[2] + " " + tokens[3]
                self.replacement = tokens[4]

        elif tokens[0] == 'f':  # Simple search
            self.fr = False
            pattern = tokens[1]

            if len(tokens) > 2 and tokens[2] == '|':
                pattern += " " + tokens[2] + " " + tokens[3]

        # Assign values to flags
        self.g = 'g' in tokens[2:]  # First or all occurrences
        self.i = 'i' in tokens[2:]  # Case sensitivity

        return pattern

    # Find a pattern of the corresponding way
    def search(self, pattern):
        # Use only lower case if 'i' is activated
        if self.i is True:
            self.searcher.set_text(self.text.lower())
            pattern = pattern.lower()
        else:
            self.searcher.set_text(self.text)

        # # Logical or (match with left or right) Example: abc | fg*i
        if '|' in pattern:
            occurrences = self.or_search(pattern)
            return occurrences

        # Simple Search: abcd
        if not any(char in pattern for char in ['[', '-', '*', '?', '|', '{']):
            occurrences = self.simple_search(pattern)

            if self.fr:
                self.replace(occurrences, self.get_patt_size(pattern))

            return occurrences

        # Range (letters and numbers): [a-z]bc, [4-7]34
        if '[' in pattern and ']' in pattern and '-' in pattern:
            occurrences = self.range_search(pattern)

            if self.fr:
                self.replace(occurrences, self.get_patt_size(pattern))

            return occurrences

        # Letter set: [abgs]cd
        if '[' in pattern and ']' in pattern and '-' not in pattern:
            occurrences = self.set_search(pattern)

            if self.fr:
                self.replace(occurrences, self.get_patt_size(pattern))

            return occurrences

        # Wildcard: ab*d
        if '*' in pattern:
            occurrences = self.wildcard_search(pattern)

            if self.fr:
                self.replace(occurrences, self.get_patt_size(pattern))

            return occurrences

        # Letter before the sign may or may not appear: ab?cd
        if '?' in pattern:
            occurrences = self.questionm_search(pattern)
            return occurrences

        # Repetition operator: a{5}cd -> “aaaaacd”
        if '{' in pattern:
            occurrences = self.repetition_search(pattern)

            if self.fr:
                self.replace(occurrences, self.get_patt_size(pattern))

            return occurrences

    # Call search again with each pattern in the OR
    def or_search(self, pattern):
        tokens = pattern.split()
        occurrences1 = self.search(tokens[0])
        occurrences2 = self.search(tokens[2])

        ocurr = occurrences1 + occurrences2
        return ocurr

    # In case of a simple search, pass the pattern as is
    def simple_search(self, pattern):
        if self.g is False:  # If 'g' is off, only search for the first occurrence
            occurrence = self.searcher.search_first(pattern)
            return occurrence

        occurrences = self.searcher.search(pattern)
        return occurrences

    # In case of a range, iterates through the ascii values from the first to the last element
    # And find all matches with every possible combination
    def range_search(self, pattern):
        index_start = pattern.find('[') + 1
        index_end = pattern.find(']') - 1

        first_ascii = ord(pattern[index_start])
        last_ascii = ord(pattern[index_end])

        if last_ascii < first_ascii:
            print("Error: index")
            return []

        patt_before = pattern[:index_start - 1]
        patt_after = pattern[index_end + 2:]

        if self.g is False:  # If g is off, only searches for the first occurrence
            smallest = 0xFFFFFF
            for i in range(first_ascii, last_ascii + 1):
                occurrence = self.searcher.search_first(patt_before + chr(i) + patt_after)
                if len(occurrence) > 0 and occurrence[0] < smallest:
                    smallest = occurrence[0]

            return [smallest]

        occurrences = []
        for i in range(first_ascii, last_ascii + 1):
            occurrences.extend(self.searcher.search(patt_before + chr(i) + patt_after))

        return occurrences

    # In case of a set, extracts the elements from the set, converts them into a list
    # And find the occurrences with each element of the set
    def set_search(self, pattern):
        index_start = pattern.find('[')
        index_end = pattern.find(']')
        set1 = list(pattern[index_start + 1: index_end])

        patt_before = pattern[:index_start]
        patt_after = pattern[index_end + 1:]

        if self.g is False:  # If g is off, only searches for the first occurrence
            smallest = 0xFFFFFF
            for i in range(len(set1)):
                occurrence = self.searcher.search_first(patt_before + set1[i] + patt_after)
                if len(occurrence) > 0 and occurrence[0] < smallest:
                    smallest = occurrence[0]

            return [smallest]

        occurrences = []
        for i in range(len(set1)):
            final_patt = patt_before + set1[i] + patt_after
            occurrences.extend(self.searcher.search(final_patt))

        return occurrences

    # In case of a wildcard search, finds the occurrences by searching with each possible combination
    def wildcard_search(self, pattern):
        index = pattern.find('*')
        patt_before = pattern[:index]
        patt_after = pattern[index + 1:]

        if self.g is False:  # If g is off, only searches for the first occurrence
            smallest = 0xFFFFFF

            for i in range(ord('0'), ord('9') + 1):
                occurrence = self.searcher.search_first(patt_before + chr(i) + patt_after)
                if len(occurrence) > 0 and occurrence[0] < smallest:
                    smallest = occurrence[0]

            for i in range(ord('a'), ord('z') + 1):
                occurrence = self.searcher.search_first(patt_before + chr(i) + patt_after)
                if len(occurrence) > 0 and occurrence[0] < smallest:
                    smallest = occurrence[0]

            if self.i is not True:
                for i in range(ord('A'), ord('Z') + 1):
                    occurrence = self.searcher.search_first(patt_before + chr(i) + patt_after)
                    if len(occurrence) > 0 and occurrence[0] < smallest:
                        smallest = occurrence[0]

            occurrence_space = self.searcher.search_first(patt_before + " " + patt_after)
            if occurrence_space[0] < smallest:
                smallest = occurrence_space[0]

            return [smallest]

        occurrences = []
        for i in range(ord('0'), ord('9') + 1):
            occurrences.extend(self.searcher.search(patt_before + chr(i) + patt_after))

        for i in range(ord('a'), ord('z') + 1):
            occurrences.extend(self.searcher.search(patt_before + chr(i) + patt_after))

        if self.i is not True:
            for i in range(ord('A'), ord('Z') + 1):
                occurrences.extend(self.searcher.search(patt_before + chr(i) + patt_after))

        occurrences.extend(self.searcher.search(patt_before + " " + patt_after))

        return occurrences

    # In case of a search with '?', first search for the pattern with the previous character and then without it
    def questionm_search(self, pattern):
        index = pattern.find('?')
        pattern1 = pattern[:index] + pattern[index + 1:]
        pattern2 = pattern1[:index - 1] + pattern1[index:]

        if self.g is False:  # If g is off, only searches for the first occurrence
            occurrence1 = self.searcher.search_first(pattern1)
            occurrence2 = self.searcher.search_first(pattern2)
            smallest = occurrence1
            pattern_d = pattern1

            if occurrence2 < smallest:
                smallest = occurrence2
                pattern_d = pattern2

            if self.fr:
                self.replace(smallest, len(pattern_d))

            return smallest

        occurrences1 = self.searcher.search(pattern1)
        if self.fr:
            self.replace(occurrences1, len(pattern1))

        occurrences2 = self.searcher.search(pattern2)
        if self.fr:
            self.replace(occurrences2, len(pattern2))

        occurrences1.extend(occurrences2)
        return occurrences1

    # In case of a search for a pattern with repetition, constructs the pattern with the repeated character
    def repetition_search(self, pattern):
        index = pattern.find('{')
        patt_before = pattern[:index - 1]
        patt_after = pattern[index + 3:]

        for i in range(int(pattern[index + 1])):
            patt_before += pattern[index - 1]

        final_patt = patt_before + patt_after

        if self.g is False:  # If g is off, only searches for the first occurrence
            occurrence = self.searcher.search_first(final_patt)
            return occurrence

        occurrences = self.searcher.search(final_patt)
        return occurrences

    # Replaces all occurrences, starting with the last index
    def replace(self, occurrences, length):
        occurrences.sort(reverse=True)
        new_text = self.text

        for i in occurrences:
            text_before = new_text[:i]
            text_after = new_text[i + length:]
            new_text = text_before + self.replacement + text_after

        with open(self.file, 'w') as file:
            file.write(new_text)

        self.text = new_text
        self.searcher.set_text(new_text)


regex = RegEx()
regex.main('test.txt')  # Here you can change the starting file
