
import re

# === Regular expressions ====
HTML_TAG = re.compile('<.*?>')

# === UI text ===
HERE_ARE_THE_EDITS = "Here is an example sequence of edits to get " + \
    "from the reference sentence to the hypothesis sentence:"


# === HTML FORMATTING (GENERAL) ===

# ====================
def cell_align_left(str_: str) -> str:
    """Put string into an HTML table cell with left alignment"""

    return f'<td style="text-align:left">{str_}</td>'


# ====================
def cell_align_right(str_: str) -> str:
    """Put string into an HTML table cell with right alignment"""

    return f'<td style="text-align:right">{str_}</td>'


# ====================
def bold(str_: str) -> str:
    """Make a string bold"""

    return f'<b>{str_}</b>'


# ====================
def add_class(word: str, class_: str) -> str:
    """Add an HTML class to a string"""

    return f'<span class="{class_}">' + word + '</span>'

        
# ====================
def remove_html(str_: str) -> str:
    """Remove all html tags from a string"""

    word = re.sub(HTML_TAG, '', str_)
    return word


# ====================
def remove_html_from_all(strs: list) -> list:
    """Remove htmls from all strings in list"""

    return [remove_html(str_) for str_ in strs]


# === STRINGS & GRAMMAR ===

# ====================
def sing_or_plural(word: str, number: int) -> str:
    """Add a plural s to the word if the number is not 1"""

    if number == 1:
        return word
    else:
        return word + 's'


# ====================
def is_or_are(number: int) -> str:
    """Return 'is' if the number is 1 or 'are' otherwise"""

    if number == 1:
        return 'is'
    else:
        return 'are'

# ====================
def clean_sent(sent: str) -> str:
    """Remove punctuation, etc. and convert to lowercase"""

    lower_letters = [c.lower()
                     for c in sent
                     if c.isalnum() or c == ' ']
    return ''.join(lower_letters)


# === LISTS AND MATRICES ===

# ====================
def max_len(l: list) -> int:
    """Get the maximum of the lengths of elements in a list"""

    return max([len(x) for x in l])

# ====================
def create_matrix(m,n):
    """Create an m by n matrix"""

    return [[0 for _ in range(m)] for _ in range(n)]


# === APPLICATION-SPECIFIC

# ====================
def print_levenshtein_matrix(matrix: list, backpointer_matrix: list,
                             words_ref: list, words_hyp: list):
    """Print a Levenshtein matrix with row and column headers"""

    new_matrix = create_matrix(len(matrix[0]), len(matrix))

    # Justify to the length of the longest word in either reference or
    # hypothesis
    just_amt = max(max_len(words_ref), max_len(words_ref)) + 1

    # Add blank cells
    words_ref = [''] + words_ref    # Header row
    words_hyp = ['', ''] + words_hyp    # Header column
    
    # Combine numbers and backpointers
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if backpointer_matrix[i][j]:
                new_matrix[i][j] = str(matrix[i][j]) + ' ' + \
                            str(backpointer_matrix[i][j])
    # Append header row
    new_matrix = [words_ref] + new_matrix
    # Append header column
    new_matrix = [[words_hyp[i]] + new_matrix[i]
               for i in range(len(new_matrix))]

    # Print
    for row in new_matrix:
        for cell in row:
            print(str(cell).ljust(just_amt), end='')
        print()
    

# ====================
def make_steps_and_sents_table(steps_and_sents: list) -> str:
    """Make an HTML table from a list of tuples of steps and sentences"""

    html_lines = ["<table>"]
    for step, sent in steps_and_sents:
        html_lines.append(
            f'<tr>{cell_align_right(bold(step))}<td></td></tr>')
        html_lines.append(
            f'<tr><td></td>{cell_align_left(sent)}</tr>')
    html_lines.append("</table>")

    return '\n'.join(html_lines)


# ====================
def generate_html_summary(reference, hypothesis, edits, wer):

    html = f"""
    <div class="extra-space">
        You said:<br>
        <p class="ref-text">"{reference}"</p>
    </div>
    <div class="extra-space">
        Google Web Speech API heard:<br>
        <p class="hyp-text">"{hypothesis}"</p>
    </div>
    <div class="extra-space">
        <span class="num">{edits}</span> 
         {sing_or_plural("edit", edits)} {is_or_are(edits)}
        required to get from the hypothesis sentence to the reference sentence (<a href="#" onclick="showLevenshtein();return false;">show Levenshtein matrix</a>).
    </div>
    <div class="extra-space">
        The word error rate (WER) is <span class="num">{wer}%</span>.
    </div>
    """

    return html    


# ====================
def generate_levenshtein_html(matrix: list, backpointer_matrix: list,
                             words_ref: list, words_hyp: list):
    """Generate an HTML string to display a Levenshtein matrix with
    backpointer symbols"""

    new_matrix = create_matrix(len(matrix[0]), len(matrix))
    just_amt = max(max_len(words_ref), max_len(words_ref)) + 1
    words_ref = [''] + words_ref    # Header row
    words_hyp = ['', ''] + words_hyp    # Header column
    
    # Combine numbers and backpointers
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if backpointer_matrix[i][j]:
                new_matrix[i][j] = str(matrix[i][j]) + ' ' + \
                            str(backpointer_matrix[i][j])
    # Append header row
    new_matrix = [words_ref] + new_matrix
    # Append header column
    new_matrix = [[words_hyp[i]] + new_matrix[i]
               for i in range(len(new_matrix))]

    html_lines = ['<table class="levenshtein"']
    for row in new_matrix:
        html_lines.append("<tr>")
        for cell in row:
            html_lines.append(f'<td>{cell}</td>')
        html_lines.append("</tr>")
    html_lines.append("</table>")

    return '\n'.join(html_lines)