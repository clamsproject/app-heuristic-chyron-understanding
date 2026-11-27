import json

from interpreter import clean_lines, normalize_text, split_text


def test_blank_and_code_fence_lines_are_dropped():
    text = '```\nREP DWIGHT TAKAMINE (D)\n\n   \nNo. Hilo Hamakua\n```'
    assert clean_lines(text) == ['REP DWIGHT TAKAMINE (D)', 'No. Hilo Hamakua']
    assert clean_lines('```text\nA\n```') == ['A']


def test_fenced_and_plain_text_give_the_same_record():
    plain = 'REP DWIGHT TAKAMINE (D)\n\nNo. Hilo Hamakua'
    fenced = f'```\n{plain}\n```'
    assert split_text(fenced, True) == split_text(plain, True)
    record = json.loads(split_text(plain, True))
    assert record == {'name-as-written': 'REP DWIGHT TAKAMINE (D)',
                      'name-normalized': 'Takamine, Rep Dwight',
                      'attributes': ['No. Hilo Hamakua']}


def test_note4_mode_takes_the_second_line_as_normalized_name():
    record = json.loads(split_text('SEN. PATTY MURRAY\nMurray, Patty\n'
                                   '(D) Washington', False))
    assert record == {'name-as-written': 'SEN. PATTY MURRAY',
                      'name-normalized': 'Murray, Patty',
                      'attributes': ['(D) Washington']}


def test_normalize_text():
    assert normalize_text('JAMES C. THOMSON') == 'Thomson, James C.'
    assert normalize_text('George Mavrothalassitis') \
        == 'Mavrothalassitis, George'
