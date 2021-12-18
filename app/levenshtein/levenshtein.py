
from levenshtein.levenshtein_helper import *
from time import sleep
import os

# ====================
def get_edit_steps(words_ref, words_hyp, backpointer_matrix):
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
def get_steps_and_sents(words_hyp, steps):
    """Given a hypothesis sentence and a sequence of steps to get to the
    reference sentence, generate a list of tuples (step, sent) that
    illustrates the steps taken to get to the reference sentence."""

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
def get_wer(reference: str, hypothesis: str) -> tuple:
    """Get number of errors and word error rate between reference and
    hypothesis transcriptions.

    Return a tuple: (edits, len_hyp, wer) edits: number of edits required
    len_ref: length of the reference sentence in words wer: word error rate as
    a percentage"""

    # === Get words from reference and hypothesis sentences ===

    words_ref = clean_sent(reference).split()
    words_hyp = clean_sent(hypothesis).split()

    # === Create separate matrices for edit distances and backpointers ===

    n = len(words_hyp) + 1
    m = len(words_ref) + 1
    matrix = create_matrix(m, n)
    backpointer_matrix = create_matrix(m, n)

    # === Initialize first row ===

    for m_ in range(m):
        matrix[0][m_] = m_

    # === Initialize first column ===

    for n_ in range(n):
        matrix[n_][0] = n_

    # === Populate remainder of matrix ===

    for n_ in range(1, n):
        for m_ in range(1, m):
            # Get distances from cells corresponding to each possible edit
            edit_options = [
                (matrix [ n_ - 1 ] [ m_ - 1 ], '⭦'),  # substitution
                (matrix [ n_ - 1 ] [ m_     ], '⭡'),  # deletion
                (matrix [ n_     ] [ m_ - 1 ], '⭠')   # insertion
            ]
            # Find the minimum of the three distances
            min_, backpointer = min(edit_options)
            # If the words in the reference and hypothesis sentences match,
            # don't make any edits. No edit is indicated with ★
            if words_ref[m_-1] == words_hyp[n_-1]:
                matrix[n_][m_] = min_
                backpointer_matrix[n_][m_] = '★'
            # If the words in the reference and hypothesis sentences are
            # different, make an appropriate edit and add one to the distance.
            else:
                matrix[n_][m_] = min_ + 1
                backpointer_matrix[n_][m_] = backpointer

    # === Get the edit steps and generate an HTML table to illustrate them ===

    steps = get_edit_steps(words_ref, words_hyp, backpointer_matrix)
    steps_and_sents = get_steps_and_sents(words_hyp, steps)
    steps_table = make_steps_and_sents_table(steps_and_sents)
    html_steps = f"""
    <div class="extra-space">
        {HERE_ARE_THE_EDITS}<br><br>
        {steps_table}
    </div>
    """

    # === Generate the final HTML to display to the user ===

    edits = matrix[n-1][m-1]
    wer = f'{edits/len(words_ref)*100:.1f}'

    html_summary = generate_html_summary(reference, hypothesis, edits, wer)

    html_parts = [html_summary]
    if edits:
        html_parts.append(html_steps)
    html = '\n'.join(html_parts)
    
    return html


# ====================
if __name__ == "__main__":

    reference = "These slides are for a phonetics class."
    hypothesis = "is lighter for a Fighters class"
    get_wer(reference, hypothesis)
