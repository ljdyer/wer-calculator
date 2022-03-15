import re

HTML_TAG = re.compile('<.*?>')

# ====================
def cell_align(str_: str, alignment: str) -> str:
    """Put string into an HTML table cell with the specified alignment"""

    return f'<td style="text-align:{alignment}">{str_}</td>'


# ====================
def bold(str_: str) -> str:
    """Make a string bold"""

    return f'<b>{str_}</b>'


# ====================
def add_class(word: str, class_: str) -> str:
    """Add an HTML class to a string"""

    return f'<span class="{class_}">' + word + '</span>'


# ====================
def remove_html(str_: str) -> str:
    """Remove all HTML tags from a string"""

    word = re.sub(HTML_TAG, '', str_)
    return word


# ====================
def remove_html_from_all(strs: list) -> list:
    """Remove HTML from all strings in list"""

    return [remove_html(str_) for str_ in strs]
