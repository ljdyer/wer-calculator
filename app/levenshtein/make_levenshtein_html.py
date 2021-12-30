import re

# === Regular expression ====

HTML_TAG = re.compile('<.*?>')

# === UI text ===

HERE_ARE_THE_EDITS = "Here is an example sequence of edits to get " + \
    "from the reference sentence to the hypothesis sentence:"
LEVENSHTEIN_LINK = \
    '<a href="#" onclick="showLevenshtein();return false;">' + \
    'show Levenshtein matrix</a>'


# === HTML FORMATTING (GENERAL) ===

# ====================
def cell_align(str_: str, alignment: str) -> str:
    """Put string into an HTML table cell with the specified alignment"""

    return f'<td style="text-align:{alignment}">{str_}</td>'


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
    """Remove all HTML tags from a string"""

    word = re.sub(HTML_TAG, '', str_)
    return word


# ====================
def remove_html_from_all(strs: list) -> list:
    """Remove HTML from all strings in list"""

    return [remove_html(str_) for str_ in strs]


# === GRAMMAR ===

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


# === LISTS AND MATRICES ===

# ====================
def create_matrix(m,n):
    """Create an m by n matrix"""

    return [[0 for _ in range(m)] for _ in range(n)]


# === MAIN FUNCTIONS ===

# ====================
def generate_html_summary(reference: str, hypothesis: str,
                          words_ref: list, words_hyp: list,
                          edits: int, wer: float,
                          backpointer_matrix: list) -> dict:

    steps_table = make_steps_and_sents_table(
        words_ref, words_hyp, backpointer_matrix)

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
        required to get from the hypothesis sentence to the reference
        sentence ({LEVENSHTEIN_LINK}).
    </div>
    <div class="extra-space">
        The word error rate (WER) is <span class="num">{wer}%</span>.
    </div>
    """
    if edits:
        html = html + f"""
        <div class="extra-space">
            {HERE_ARE_THE_EDITS}<br><br>
            {steps_table}
        </div>
        """

    return html


# ====================
def make_steps_and_sents_table(words_ref: list, words_hyp: list,
                   backpointer_matrix: list) -> str:
    """Make an HTML table that shows a series of steps to get from
    a hypothesis to a reference transcription"""

    steps_and_sents = get_steps_and_sents(
        words_ref, words_hyp, backpointer_matrix)

    html_lines = ["<table>"]
    for step, sent in steps_and_sents:
        html_lines.append(
            f'<tr>{cell_align(bold(step), "right")}<td></td></tr>')
        html_lines.append(
            f'<tr><td></td>{cell_align(sent, "left")}</tr>')
    html_lines.append("</table>")

    steps_table = '\n'.join(html_lines)

    return steps_table


# ====================
def get_edit_steps(words_ref: list, words_hyp: list,
                   backpointer_matrix: list) -> list:
    """Given reference and hypothesis sentences and the matrix of backpointers
    from the Levenshtein algorithm, find an appropriate sequence of steps to
    get from the reference sentence to the hypothesis sentence."""

    # Start at bottom right of matrix. Rows represent words in the hypothesis
    # sentence and columns represent words in the reference sentence.
    row = len(backpointer_matrix) - 1
    col = len(backpointer_matrix[0]) - 1
    steps = []

    # Traverse matrix from right to left and bottom to top in route indicated
    # by backpointers, adding edit steps as we go
    while row > 0 and col > 0:
        this_backpointer = backpointer_matrix[row][col]
        if this_backpointer == '★':
            row -= 1
            col -= 1
            steps.insert(0, ('KEEP', words_hyp[row]))
        elif this_backpointer == '⭦':
            row -= 1
            col -= 1
            steps.insert(0, ('SUB', words_hyp[row], words_ref[col]))
        elif this_backpointer == '⭠':
            col -= 1
            steps.insert(0, ('INS', words_ref[col]))
        elif this_backpointer == '⭡':
            row -= 1
            steps.insert(0, ('DEL', words_hyp[row]))

    return steps


# ====================
def get_steps_and_sents(words_ref: list, words_hyp: list,
                        backpointer_matrix: list) -> list:
    """Given a hypothesis sentence and a sequence of steps to get to the
    reference sentence, generate a list of tuples (step, sent) that
    illustrates the steps taken to get to the reference sentence."""

    # Get the edit steps
    steps = get_edit_steps(words_ref, words_hyp, backpointer_matrix)

    # Start with the hypothesis sentence
    latest_sentence = words_hyp.copy()
    steps_and_sents = []

    for i, s in enumerate(steps):

        # Remove word highlights from previous step
        latest_sentence = remove_html_from_all(latest_sentence)

        if s[0] == "SUB":
            step = f"substitute: '{s[1]}' ⭢  '{s[2]}'"
            latest_sentence[i] = add_class(s[2], 'sub')
            sentence = ' '.join(latest_sentence)
            steps_and_sents.append((step, sentence))

        if s[0] == "INS":
            step = f"insert: '{s[1]}'"
            latest_sentence.insert(i, add_class(s[1], 'ins'))
            sentence = ' '.join(latest_sentence)
            steps_and_sents.append((step, sentence))

        if s[0] == "DEL":
            step = f"delete: '{s[1]}'"
            latest_sentence.remove(s[1])
            sentence = ' '.join(latest_sentence)
            steps_and_sents.append((step, sentence))

    return steps_and_sents


# ====================
def generate_levenshtein_html(matrix: list, backpointer_matrix: list,
                             words_ref: list, words_hyp: list):
    """Generate an HTML string to display a Levenshtein matrix with
    backpointer symbols"""

    new_matrix = create_matrix(len(matrix[0]), len(matrix))
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