"""
Heuristic Chyron Understanding (prototype)

Converts chyron text from docTR/Tesseract/LLaVA MMIF output into a name and list of attributes.
"""

import argparse
import logging

from clams import ClamsApp, Restifier
from mmif import Mmif, DocumentTypes

import interpreter

class HeuristicChyronInterpreter(ClamsApp):

    def __init__(self):
        super().__init__()
        # Currently no CUDA implementation.

    def _appmetadata(self):
        # using metadata.py
        pass

    def _annotate(self, mmif: Mmif, **parameters) -> Mmif:

        self.mmif = mmif if isinstance(mmif, Mmif) else Mmif(mmif)

        new_view = self.mmif.new_view()
        new_view.metadata.app = self.metadata.identifier
        self.sign_view(new_view, parameters)
        new_view.new_contain(DocumentTypes.TextDocument)

        for doc in self.mmif.get_documents_by_type(DocumentTypes.TextDocument):
            self._run_interpreter(doc, new_view)

        return self.mmif

    def _run_interpreter(self, doc, new_view):
        """
        Run the chyron interpreter over the document and add annotations to the view.
        """
        text = doc.text_value
        content = interpreter.split_text(text)
        mmif_vids = self.mmif.get_documents_by_type(DocumentTypes.VideoDocument)
        vid_id = mmif_vids[0].long_id
        out_doc = new_view.new_textdocument(text=content, document=vid_id, origin=doc.long_id)
        out_doc.add_property('provenance', 'derived')
        out_doc.add_property('mime', 'application/json')

def get_app():
    """
    Create an instance of the app class.
    """
    return HeuristicChyronInterpreter()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", default="5000", help="set port to listen")
    parser.add_argument("--production", action="store_true", help="run gunicorn server")

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
