"""
The purpose of this file is to define the metadata of the app with minimal imports.

DO NOT CHANGE the name of the file
"""

from mmif import DocumentTypes

from clams.app import ClamsApp
from clams.appmetadata import AppMetadata


# DO NOT CHANGE the function name
def appmetadata() -> AppMetadata:
    """
    Function to set app-metadata values and return it as an ``AppMetadata`` obj.
    Read these documentations before changing the code below
    - https://sdk.clams.ai/appmetadata.html metadata specification.
    - https://sdk.clams.ai/autodoc/clams.appmetadata.html python API
    
    :return: AppMetadata object holding all necessary information.
    """
    metadata = AppMetadata(
        name="Heuristic Chyron Understanding",
        description="Prototype to convert chyron text from docTR/Tesseract/LLaVA MMIF output"
                    "into a name and list of attributes.",
        app_license="Apache 2.0",
        identifier="heuristic-chyron-understanding",
        url="https://github.com/clamsproject/app-heuristic-chyron-understanding",
    )

    # I/O Spec
    in_doc = metadata.add_input(DocumentTypes.TextDocument)
    in_doc.add_description('Text content transcribed from video input by docTR/Tesseract/LLAVA.')
    out_doc = metadata.add_output(DocumentTypes.TextDocument, **{'document': '*', 'origin': '*'})
    out_doc.add_description('Reformatted chyron text. `document` property stores the ID of the original source '
                            '`VideoDocument`. `origin` property stores the ID of the original OCR `TextDocument` '
                            'annotation. ')
    
    # No runtime parameters besides universals.

    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    metadata = appmetadata()
    for param in ClamsApp.universal_parameters:
        metadata.add_parameter(**param)
    sys.stdout.write(metadata.jsonify(pretty=True))
