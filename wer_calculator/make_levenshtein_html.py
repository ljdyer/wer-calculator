from helper.helper import create_matrix
from helper.html_helper import add_class, remove_html_from_all
from helper.grammar_helper import is_or_are, sing_or_plural
from jinja2 import Environment, PackageLoader


# ====================
def generate_html_summary(reference: str, hypothesis: str,
                          words_ref: list, words_hyp: list,
                          edits: int, wer: float,
                          backpointer_matrix: list) -> dict:

    steps_and_sents = get_steps_and_sents(
        words_ref, words_hyp, backpointer_matrix)

    env = Environment(
        loader=PackageLoader("make_levenshtein_html"),
    )
    template = env.get_template('wer_info.html')

    html = template.render(
        ref_text=reference,
        hyp_text=hypothesis,
        num_edits=edits,
        edit_or_edits=sing_or_plural("edit", edits),
        is_or_are=is_or_are(edits),
        wer=wer,
        steps_and_sents=steps_and_sents
    )

    return html


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
                new_matrix[i][j] = ' '.join([
                    str(matrix[i][j]),
                    str(backpointer_matrix[i][j])
                ])
    # Append header row
    new_matrix = [words_ref] + new_matrix
    # Append header column
    new_matrix = [[words_hyp[i]] + new_matrix[i]
                  for i in range(len(new_matrix))]

    env = Environment(
        loader=PackageLoader("make_levenshtein_html"),
    )
    template = env.get_template('levenshtein_matrix.html')

    html = template.render(
        new_matrix=new_matrix
    )

    return html
