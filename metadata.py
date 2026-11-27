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
        description="Prototype to convert chyron text from OCR output "
                    "(e.g., docTR, Tesseract or a VLM captioner) into a "
                    "name and list of attributes, with line-based "
                    "heuristics.",
        app_license="Apache 2.0",
        identifier="heuristic-chyron-understanding",
        url="https://github.com/clamsproject/app-heuristic-chyron-understanding",
    )

    # I/O Spec
    in_doc = metadata.add_input(DocumentTypes.TextDocument)
    in_doc.add_description(
        'Chyron text transcribed by an OCR app. The app reads the '
        'TextDocuments of the last view that has any; without such a view, '
        'the top-level TextDocuments of the MMIF. Empty texts and "no text" '
        'markers (e.g., `NONE`, `N/A`) are skipped, and markdown code fence '
        'lines (e.g., "```") around the text are ignored.')
    out_doc = metadata.add_output(
        DocumentTypes.TextDocument, document='*', origins='*',
        origination='derived', mime='application/json')
    out_doc.add_description(
        'Reformatted chyron text, one per input TextDocument: a JSON string '
        'with three fields, `name-as-written`, `name-normalized` and '
        '`attributes`. The `origins` property points to the input OCR '
        'TextDocument; `document` is copied from it, or else is the ID of '
        'the source `VideoDocument`.')
    
    metadata.add_parameter(name='note4mode', default=False, type='boolean',
                           description='Boolean to set the app to run in "note-4" mode and to take the second line '
                                       '(if available) from the input text to be the `name-normalized` value. The '
                                       'default is false, which means the app will try to generate normalization from'
                                       '`name-as-written` (from the first line) value. ')

    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    metadata = appmetadata()
    for param in ClamsApp.universal_parameters:
        metadata.add_parameter(**param)
    sys.stdout.write(metadata.jsonify(pretty=True))
