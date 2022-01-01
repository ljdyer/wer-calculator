from levenshtein.make_levenshtein_html \
    import generate_html_summary, generate_levenshtein_html

# ====================
def create_matrix(m,n):
    """Create an m by n matrix"""

    return [[0 for _ in range(m)] for _ in range(n)]


# ====================
def clean_sentence(sent: str) -> str:
    """Remove punctuation, etc. and convert to lowercase"""

    lower_letters = [c.lower()
                     for c in sent
                     if c.isalnum() or c == ' ']
    return ''.join(lower_letters)


# ====================
def get_wer_info(words_ref: list, words_hyp: list) -> dict:
    """Given lists of words in the reference and hypothesis transcriptions,
    calculate the minimum edit distance and word error rate between
    them using the Levenshtein algorithm.

    Return a dictionary with 4 elements:

    'edits': The minimum edit distance
    'wer': The word error rate as a percentage rounded to one decimal
           place
    'matrix': The levenshtein matrix with scores used to calculate
              minimum edits
    'backpointer_matrix': The matrix with backpointers used to find a
                          possible series of edits
    """

    # Create separate matrices for edit distances and backpointers
    n = len(words_hyp) + 1
    m = len(words_ref) + 1
    matrix = create_matrix(m, n)
    backpointer_matrix = create_matrix(m, n)

    # Initialize first row
    for m_ in range(m):
        matrix[0][m_] = m_

    # Initialize first column
    for n_ in range(n):
        matrix[n_][0] = n_

    # Populate remainder of matrix
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

    # Get minimum edit distance and WER
    edits = matrix[n-1][m-1]
    wer = float(f'{edits/len(words_ref)*100:.1f}')

    return {
        'edits': edits,
        'wer': wer,
        'matrix': matrix,
        'backpointer_matrix': backpointer_matrix
    }


# ====================
def get_levenshtein_html(reference: str, hypothesis: str) -> dict:
    """Get HTML for information about WER to display to the user

    Return a dictionary with two elements:

    'html': The HTML for the main part of the page that includes
            information about WER and edit sequence
    'levenshtein': The HTML for the modal popup that shows the
                   Levenshtein matrix
    """

    # Get words from reference and hypothesis sentences
    words_ref = clean_sentence(reference).split()
    words_hyp = clean_sentence(hypothesis).split()

    # Get WER and Levenshtein matrices
    wer_info = get_wer_info(words_ref, words_hyp)
    edits = wer_info['edits']
    wer = wer_info['wer']
    matrix = wer_info['matrix']
    backpointer_matrix = wer_info['backpointer_matrix']

    # Generate table showing the a series of steps to get from
    # reference to hypothesis sentence
    
    # Generate the final HTML to display to the user
    html = generate_html_summary(
        reference, hypothesis, words_ref, words_hyp,
        edits, wer, backpointer_matrix)
    levenshtein_html = generate_levenshtein_html(
        matrix, backpointer_matrix, words_ref, words_hyp)

    return {'html': html, 'levenshtein': levenshtein_html}