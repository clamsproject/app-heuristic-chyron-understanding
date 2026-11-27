"""
Heuristic Chyron Understanding (prototype)

Converts chyron text from OCR output (e.g., docTR, Tesseract or a VLM
captioner) into a name and list of attributes.
"""

import argparse
import logging
from typing import List

from clams import ClamsApp, Restifier
from mmif import Mmif, DocumentTypes

import interpreter

# input texts read as "no text" (e.g., an OCR step's answer for a frame
# without text), compared after stripping whitespace and trailing periods,
# case-insensitively
NO_TEXT_MARKERS = frozenset({'', 'NONE', 'NULL', 'N/A', 'NA', 'NO TEXT', '-'})


def is_no_text(text: str) -> bool:
    return text.strip().rstrip('.').strip().upper() in NO_TEXT_MARKERS


class HeuristicChyronInterpreter(ClamsApp):

    def __init__(self):
        super().__init__()

    def _appmetadata(self):
        # using metadata.py
        pass

    @staticmethod
    def select_inputs(mmif: Mmif) -> List:
        """
        The TextDocuments of the last view that has any (the OCR output),
        or the top-level TextDocuments when no view has one; empty texts
        and "no text" markers are left out.
        """
        views = mmif.get_all_views_contain(DocumentTypes.TextDocument)
        if views:
            docs = list(views[-1].get_annotations(DocumentTypes.TextDocument))
        else:
            docs = [d for d in mmif.documents
                    if d.at_type == DocumentTypes.TextDocument]
        return [d for d in docs if not is_no_text(d.text_value)]

    def _annotate(self, mmif: Mmif, **parameters) -> Mmif:
        # select inputs before adding the new view, which also contains
        # TextDocuments
        inputs = self.select_inputs(mmif)
        new_view = mmif.new_view()
        self.sign_view(new_view, parameters)
        new_view.new_contain(DocumentTypes.TextDocument,
                             origination='derived', mime='application/json')
        videos = mmif.get_documents_by_type(DocumentTypes.VideoDocument)
        default_medium = videos[0].long_id if videos else None
        normalize = not parameters['note4mode']
        for doc in inputs:
            content = interpreter.split_text(doc.text_value, normalize)
            td = new_view.new_textdocument(text=content)
            td.add_property('origins', [doc.long_id])
            medium = doc.get_property('document') or default_medium
            if medium:
                td.add_property('document', medium)
        return mmif


def get_app():
    """
    Create an instance of the app class.
    """
    return HeuristicChyronInterpreter()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", default="5000",
                        help="set port to listen")
    parser.add_argument("--production", action="store_true",
                        help="run gunicorn server")

    parsed_args = parser.parse_args()

    # create the app instance
    app = get_app()

    http_app = Restifier(app, port=int(parsed_args.port))
    # for running the application in production mode
    if parsed_args.production:
        http_app.serve_production()
    # development mode
    else:
        app.logger.setLevel(logging.DEBUG)
        http_app.run()
