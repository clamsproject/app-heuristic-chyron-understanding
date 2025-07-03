"""
Chyron Interpreter (prototype)

Reformats chyron text output from an OCR app as a name and list of attributes
presented as an escaped json string.
"""

__VERSION__ = 'v0.1'

import json

def split_text(text: str) -> str:
    """
    Splits input string on newline and creates a dictionary with 'name-as-written'
    and 'attributes' keys, with string content as values.
    Returns escaped json string of dictionary.
    """
    content = {}
    lines = text.split("\n")
    if lines:
        content["name-as-written"] = lines[0]
        content["attributes"] = [x for x in lines[1:] if x != '']
    content = json.dumps(content)

    return content