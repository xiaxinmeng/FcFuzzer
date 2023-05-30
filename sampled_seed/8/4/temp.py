IPV4_RE = re.compile('\\.\\d+$', re.ASCII)

def is_HDN(text):
    """Return True if text is a host domain name."""
    if IPV4_RE.search(text):
        return False
    if text == '':
        return False
    if text[0] == '.' or text[-1] == '.':
        return False
    return True