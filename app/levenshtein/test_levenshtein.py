from levenshtein.levenshtein import clean_sentence, get_wer_info

# Expected values obtained from https://www.amberscript.com/en/wer-tool/

TEST_CASES = [
    {
        'reference': 'These slides are for a phonetics class.',
        'hypothesis': 'These slides are for a phonetics class',
        'wer': 0
    },
    {
        'reference': 'These slides are for a phonetics class.',
        'hypothesis': 'this slider for a phonetics class',
        'wer': 42.9
    },
    {
        'reference': 'These slides are for a phonetics class.',
        'hypothesis': 'this is a sentence that has absolutely nothing to do with the reference sentence',
        'wer': 200
    },
    # If hypothesis is empty, WER is 100%
    {
        'reference': 'These slides are for a phonetics class.',
        'hypothesis': '',
        'wer': 100
    }
]

# Exception should be raised if reference sentence is empty (division by zero)
ERROR_CASE = {
    'reference': '',
    'hypothesis': 'These slides are for a phonetics class.',
}


# ====================
def test_get_wer_info():
    """Run test cases for get_wer_info function"""

    # Print a warning and exit if get_wer_info returns a different
    # WER to the expected WER for any of the test cases
    for tc in TEST_CASES:
        words_ref = clean_sentence(tc['reference']).split()
        words_hyp = clean_sentence(tc['hypothesis']).split()
        wer_info = get_wer_info(words_ref, words_hyp)
        try:
            assert wer_info['wer'] == tc['wer']
        except:
            print(wer_info['wer'])
            print('!!! WARNING !!!: test_get_wer_info failed for',
                  f'reference: {tc["reference"]};',
                  f'hypothesis: {tc["hypothesis"]}.')
            quit()

    # Print a warning and exit if get_wer_info does not raise
    # an exception when the hypothesis sentence is empty
    words_ref = clean_sentence(ERROR_CASE['reference']).split()
    words_hyp = clean_sentence(ERROR_CASE['hypothesis']).split()
    try:
        wer_info = get_wer_info(words_ref, words_hyp)
        print('!!! WARNING !!!: test_get_wer_info did not raise an',
              'exception when hypothesis=""')
        quit()
    except:
        pass

    # If we made it to the end without quitting, all tests were
    # passed
    print('*** test_get_wer_info: All tests passed. ***')