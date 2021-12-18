
import re
HTML_TAG = re.compile('<.*?>')
HERE_ARE_THE_EDITS = "Here are the edits required to get " + \
    "from the reference sentence to the hypothesis sentence:"

# ====================
def cell_align_left(str_: str) -> str:
    """Put string into an HTML table cell with left alignment"""

    return f'<td style="text-align:left">{str_}</td>'


# ====================
def cell_align_right(str_: str) -> str:
    """Put string into an HTML table cell with right alignment"""

    return f'<td style="text-align:right">{str_}</td>'


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
def create_matrix(m,n):
    """Create an m by n matrix"""

    return [[0 for _ in range(m)] for _ in range(n)]


# ====================
def clean_sent(sent: str) -> str:
    """Remove punctuation, etc. and convert to lowercase"""

    lower_letters = [c.lower()
                     for c in sent
                     if c.isalnum() or c == ' ']
    return ''.join(lower_letters)


# ====================
def max_len(l: list) -> int:
    """Get the maximum of the lengths of elements in a list"""

    return max([len(x) for x in l])


# ====================
def print_levenshtein_matrix(matrix: list, row_header: list,
                             col_header: list):
    """Print a Levenshtein matrix with row and column headers"""

    row_header = ['', ''] + row_header

    just_amt = max(max_len(row_header), max_len(col_header)) + 1

    # os.system('cls')
    for col in row_header:
        print(f'{col.ljust(just_amt)}', end='')
    print()
    print()
    for i in range(len(matrix)):
        if i > 0:
            print(f'{col_header[i-1].ljust(just_amt)}', end='')
        else:
            print(f'{"".ljust(just_amt)}', end='')
        for col in matrix[i]:
            print(f'{str(col).ljust(just_amt)}', end='')
        print()
        print()


# ====================
def add_class(word: str, class_: str) -> str:
    """Add an HTML class to a word"""

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


# ====================
def make_html_table(table: list) -> str:
    """Make an HTML table from a list of lists"""



    html_lines = ["<table>"]
    for step, sent in table:
        html_lines.append(
            f'<tr>{cell_align_right(step)}<td></td></tr>')
        html_lines.append(
            f'<tr><td></td>{cell_align_left(sent)}</tr>')
    html_lines.append("</table>")

    return '\n'.join(html_lines)


# ====================
def generate_html_summary(reference, hypothesis, edits, wer):

    html_lines = [
        "============================================",
        "<div>",
        "You said:<br><br>",
        f'<span class="ref-text">"{reference}"</span>',
        "</div>",
        "<div>",
        "Google Web Speech API heard:<br><br>",
        f'<span class="hyp-text">"{hypothesis}"</span>',
        "</div>",
        "<div>",
        f'<span class="num">{edits}</span> {sing_or_plural("edit", edits)} {is_or_are(edits)} ' + \
            'required to get from the hypothesis sentence to the reference sentence.',
        "</div>",
        "<div>",
        f'The word error rate (WER) is <span class="num">{wer}%</span>.'
        "</div>",
    ]
    return '\n'.join(html_lines)
    
