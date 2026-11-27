"""
Chyron Interpreter (prototype)

Reformats chyron text output from an OCR app as a name and list of attributes
presented as an escaped json string.
"""

import json
import re

# a markdown code fence line (e.g., "```" or "```text"), which some VLMs
# wrap around their transcriptions
CODE_FENCE = re.compile(r'^\s*```[\w-]*\s*$')


def clean_lines(text: str) -> list:
    """
    Splits OCR text into lines, leaving out blank lines and markdown code
    fence lines.
    """
    return [line for line in text.split("\n")
            if line.strip() and not CODE_FENCE.match(line)]


def split_text(text: str, normalize=False) -> str:
    """
    Splits input string on newline and creates a dictionary with 'name-as-written'
    and 'attributes' keys, with string content as values. If normalization parameter
    is True, also adds a 'name-normalized' item to the dictionary.
    Returns escaped json string of dictionary.
    """
    content = {}
    lines = clean_lines(text)
    if lines:
        content["name-as-written"] = lines[0]
        if normalize:
            content["name-normalized"] = normalize_text(lines[0])
            last_line_processed = 0
        else:
            if len(lines) > 1:
                content["name-normalized"] = lines[1]
                last_line_processed = 1
            else:
                content["name-normalized"] = ''
                last_line_processed = 0
        content["attributes"] = lines[(last_line_processed+1):]
    content = json.dumps(content)

    return content


def normalize_text(text: str) -> str:
    """
    Converts input string to a 'normalized' name form.
    Returns text in a 'Lastname, Firstname' format.
    """
    # Depending on the quality of the OCR, this may not represent the original chyron as well as desired.

    # strip whitespace first to avoid complicating the regex
    text = text.strip()

    # remove common parenthetical content like (D)
    p_close = r'..\)'
    p_open = r'\(..'
    text = re.sub(p_close, ' ', text)
    text = re.sub(p_open, ' ', text)

    # remove extraneous dashes (without clipping properly hyphenated names)
    dash = r'(\s*-\s+)|(\s+-\s*)|^-|-$'
    text = re.sub(dash, ' ', text)

    # remove various non-letter characters that appear
    punc = r'[,#*@:[]'
    text = re.sub(punc, ' ', text)

    # remove numbers from beginning of text
    num = r'\A[0-9]+'
    text = re.sub(num, ' ', text)

    # remove patterns up to and incl. a period NOT at end of string
    # handles e.g. Sen. XYZ without removing XYZ Jr. or initials like ABC F. XYZ
    abb = r'[^\s.]{2,}\.(?=.)'
    text = re.sub(abb, ' ', text)

    # and split initials like A.B. into A. B.
    inits = r'([A-Za-z]\.){2,}'
    target = re.search(inits, text)
    if target:
        start_idx = target.span()[0]
        end_idx = target.span()[1]
        splt = re.sub(r'\.(?=.)', '. ', target.group())
        text = ''.join([text[0:start_idx], splt, text[end_idx:]])

    # remove any extraneous whitespace added before splitting
    text = text.strip()
    parts = text.split()

    normal_name = ""
    normal_parts = []
    for word in parts:
        word = ''.join([word[0].upper(), word[1:].lower()])
        normal_parts.append(word)

    if len(normal_parts) == 1:
        normal_name = normal_parts[0]
    elif len(normal_parts) > 1:
        normal_name = normal_parts[-1] + ', ' + ' '.join(normal_parts[:-1])

    return normal_name