from libsbml import SBMLValidator as validator
from libsbml import SBMLReader
from libsbml import SBMLDocument


def validate_sbml(file_string):
    doc = SBMLReader.readSBMLFromString(SBMLReader(), file_string)
    val = validator()
    val.setDocument(doc)
    a = val.validate()
    failures = val.getNumFailures()

    if failures > 0:
        error_message = ""
        for i in range(failures):
            error_message += val.getFailure(i).getMessage() + "\n"
        return error_message

    return a
