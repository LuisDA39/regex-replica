# regex-replica

Custom RegEx is a modified version of regular expressions, designed to handle seven specific cases and two flags. It accepts only one pattern per search, except when using the OR operator (`|`). This project provides a simple yet powerful way to search and replace patterns within text files.

## How It Works

In this modified RegEx implementation, we support the following cases:

1. **Simple Search**: Input a query to find an exact match in the text, e.g., `write`.
2. **Ranges**: Enclose a range in square brackets, e.g., `[a-z]p`, which matches any letter from `a` to `z` followed by a `p` (e.g., `up`).
3. **Sets**: Enclose characters in square brackets, e.g., `[asd]e`, which matches any of the characters `a`, `s`, or `d` followed by an `e` (e.g., `ae`, `se`, `de`).
4. **Question Mark**: The preceding character may or may not exist. For example, `of?f` matches `of` and `off`.
5. **Asterisk**: Acts as a wildcard representing any character. For example, `*n` matches `in`, ` n`, `0n`.
6. **Pipe (OR) Operator (`|`)**: Matches the pattern on the left or the pattern on the right.
7. **Repetition Operator (`{}`)**: A character followed by a number in curly braces specifies how many times the character should be repeated. For instance, `s{2}ion` matches `ssion`.

The flags are:
- **`g`**: Apply the search or replace operation globally across all matches in the text.
- **`i`**: Perform the operation case-insensitively.

## Usage

1. Enter your search query in the correct format.
2. Click the "Search" button.
   - For a simple search, all occurrences will be highlighted.
   - For search and replace, occurrences will be replaced.
3. The number of occurrences found will be displayed below the search button.

## Changing the Input File

To change the file being read, locate the `RegEx()` class instance at the end of the main file and call the `main` function. Inside this function, specify the name of the file where searches should be performed.

# Search Format

Searches should be formatted as follows:

- `f <pattern> [flags]`

Example: `f ab?c g`

## Search and Replace Format

For search and replace, format as follows:

- `fr <pattern_to_replace> <replacement_pattern> [flags]`

Example: `fr up*u g i`

## Using the Or Operator (`|`)

To use the OR operator, separate patterns with `|`:

- `f <pattern1> | <pattern2> [flags]`

Example: `f j*l | you i g` and `fr [e-p]h | [kno]y g`

**Note:** There must be a space between each command/term.

## RegEx Class

The `RegEx` class provides the user interface for searching and replacing patterns in a text file, handling all configurations and operations based on user input.

### `main()` and `set_text()`

- **`main()`**: Controls the graphical interface and receives the text file for search operations. Defines the `search` function for processing queries.
- **`set_text()`**: Loads the content of the text file into `self.text`, enabling search and replace operations.

### `get_patt_size()`

Calculates the actual length of a pattern, excluding special symbols. Returns the length for different types of patterns and helps in processing.

### `compute_query()`

Interprets and processes the input query. Extracts the pattern and applies necessary configurations such as flags and OR operations.

### `search()`

Analyzes the pattern and applies different search strategies based on the pattern type. Returns occurrences according to the search configuration.

### Search Methods

- **Simple Search**: Searches for exact matches.
- **Range Search (`[ - ]`)**: Finds patterns within a character range.
- **Set Search (`[ ]`)**: Finds patterns with specific sets of characters.
- **Wildcard Search (`*`)**: Matches patterns containing any character.
- **Question Mark Search (`?`)**: Matches patterns with optional preceding characters.
- **Repetition Search (`{}`)**: Finds patterns with repeated characters.
- **Or Search (`|`)**: Finds patterns matching at least one of multiple specified patterns.

### `replace()`

Replaces all occurrences of a pattern in the text with a provided replacement. Updates the original file and the in-memory text.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

- [@LuisDA39](https://github.com/LuisDA39)
- [@samir-bstb](https://github.com/samir-bstb)
