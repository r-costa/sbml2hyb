from libsbml import SBMLValidator as validator


def validate_sbml(filename):
    val = validator()
    a = val.validate(filename)
    failures = val.getNumFailures()

    if failures > 0:
        error_message = ""
        for i in range(failures):
            error_message += val.getFailure(i).getMessage() + '\n'
        return error_message

    return a
