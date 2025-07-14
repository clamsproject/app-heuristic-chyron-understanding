"""
Chyron Interpreter (prototype)

Reformats chyron text output from an OCR app as a name and list of attributes
presented as an escaped json string.
"""
import json


def split_text(text: str, normalize=False) -> str:
    """
    Splits input string on newline and creates a dictionary with 'name-as-written'
    and 'attributes' keys, with string content as values. If normalization parameter
    is True, also adds a 'name-normalized' item to the dictionary.
    Returns escaped json string of dictionary.
    """
    content = {}
    lines = list(filter(lambda x: x is not None and len(x) > 0, text.split("\n")))
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

    if text.find('.') != -1: # Will only strip 1 abbreviated title, not multiple or full-word titles.
        text = text[text.find('.') + 1:]
    if text.find('(') != -1:
        text = text[:text.find('(')]
    if text.find(', ') != -1:
        text = text[:text.find(', ')]
    parts = text.split()
    normal_parts = []
    for word in parts:
        word = ''.join([word[0].upper(), word[1:].lower()])
        normal_parts.append(word)
    if len(normal_parts) == 1:
        normal_name = normal_parts[0]
    else:
        normal_name = ' '.join(normal_parts[1:]) + ', ' + normal_parts[0]  # to handle names with more than two words

    return normal_name