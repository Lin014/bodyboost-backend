
def NotFoundResponse(role):
    return { "message": role + " not found." }

def FormatErrorResponse(role):
    return { "message": role + " format error." }