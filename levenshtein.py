
# Calculate Levenshtein distance between two sentences

# ====================
def clean_sent(sent: str) -> str:
    """Remove any unusual characters and convert to lowercase"""

    lower_letters = [c.lower() for c in sent if c.isalnum() or c == ' ']
    return ''.join(lower_letters)


# ====================
def get_wer(reference: str, hypothesis: str) -> tuple:
    """Get number of errors and word error rate between reference and
    hypothesis transcriptions.
    
    Return a tuple: (edits, len_hyp, wer)
    edits: number of edits required
    len_ref: length of the reference sentence in words
    wer: word error rate as a percentage"""

    words_ref = clean_sent(reference).split()
    words_hyp = clean_sent(hypothesis).split()

    # Define matrix
    n = len(words_hyp) + 1
    m = len(words_ref) + 1
    matrix = [[0 for _ in range(n+1)] for _ in range(m+1)]

    # init first row
    for m_count in range(m):
        matrix[0][m_count] = m_count

    # init first column
    for n_count in range(n):
        matrix[n_count][0] = n_count

    for n_count in range(1,n):
        for m_count in range(1,m):
            min_ = min(
                matrix[n_count-1][m_count-1],
                matrix[n_count-1][m_count],
                matrix[n_count][m_count-1])
            if words_ref[m_count-1] == words_hyp[n_count-1]:
                matrix[n_count][m_count] = min_
            else:
                matrix[n_count][m_count] = min_ + 1

    errors = matrix[n-1][m-1]

    return (errors, len(words_ref), float(f'{errors/len(words_hyp)*100:.2f}'))


# ====================
if __name__ == "__main__":

    reference = "These slides are for a phonetics class"
    hypothesis = "please sites slider pro phonetics class"
    print(get_wer(reference, hypothesis))










