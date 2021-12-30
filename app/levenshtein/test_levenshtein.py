# Expected values calculated at https://www.amberscript.com/en/wer-tool/

test_cases = [
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
    }
]