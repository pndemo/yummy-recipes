
"""
Contains utilify functions
"""

import re

def validate_title(title):
    """ Returns True if a valid title is provided """
    title = re.sub(' +', ' ', title.strip())
    regexp = re.compile(r"^[a-zA-Z0-9-' ]*$")
    if regexp.search(title):
        return True
    return False
