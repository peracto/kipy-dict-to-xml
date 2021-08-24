import re
_escape_regex = re.compile(r"[&><\n\r\t]")
_escape_quote_regex = re.compile(r"[&><\n\r\t;]")
_replacements = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '\n': '&#10;',
    '\r': '&#13;',
    '\t': '&#9;',
    '"': '&quot;'
}


def _escape_rep(r):
    return _replacements.get(r.group(0))


def escape(data: str):
    return _escape_regex.sub(_escape_rep, data)


def quote_attr(data: str):
    return _escape_quote_regex.sub(_escape_rep, data)
