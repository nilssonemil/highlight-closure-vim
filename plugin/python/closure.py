import vim


"""
The following characters are what is considered the *opening* brackets.
"""
OPENING_BRACKETS = "{[("


"""
The following characters are what is considered the *closing* brackets.
"""
CLOSING_BRACKETS = "}])"


"""
Command to issue for setting highlight of a specifc buffer position.
"""
MATCH_POS = "call matchaddpos('BracketClosure', [[{row}, {column}]])"


def highlight_surrounding_brackets():
    """
    Highlight the brackets that surround the current cursor position. If the
    cursor is located on a bracket or if there is no surrounding brackets no
    highlighting will be done.

    Note that this function assumes that there are matching brackets. If there
    are bracket matching of different types it would be highlighted in a way
    that is probably unexpected. E.g. "def func(param1])" would highlight '('
    and ']' as matching brackets.

    '{', '[', '(', ')', ']', '}' are the characters considered brackets.
    """
    open_bracket, close_bracket = current_bracket_scope()
    if open_bracket and close_bracket:
        vim.command(MATCH_POS.format(
            row=open_bracket[0],
            column=open_bracket[1]))
        vim.command(MATCH_POS.format(
            row=close_bracket[0],
            column=close_bracket[1]))


def current_bracket_scope():
    cursor_row, cursor_col = vim.current.window.cursor

    # We already have highlighting if the cursor is on a bracket. We return
    # None and let the plugin reset the previous highlighting.
    # TODO: Change so that we extend the scope around the current brackets.
    current_row = vim.current.buffer[cursor_row-1]
    if (current_row and
        current_row[cursor_col] in OPENING_BRACKETS+CLOSING_BRACKETS):
        return (None, None)

    opening = get_opening_bracket(vim.current.buffer, cursor_row, cursor_col)
    closing = get_closing_bracket(vim.current.buffer, cursor_row, cursor_col)
    return (opening, closing)


def get_opening_bracket(_buffer, cursor_row, cursor_col):
    middle = _buffer[cursor_row-1]
    rows = _buffer[:cursor_row-1] + [middle[:cursor_col+1]]

    row_offset = 1
    col_offset = 1

    closed_brackets = 1
    for r in range(len(rows)-1, -1, -1): # loop backwards
        for c in range(len(rows[r])-1, -1, -1):
            char = rows[r][c]
            if char in CLOSING_BRACKETS:
                closed_brackets += 1
            elif char in OPENING_BRACKETS:
                closed_brackets -= 1
                if closed_brackets == 0:
                    return (r + row_offset, c + col_offset)

    return None # No match found


def get_closing_bracket(_buffer, cursor_row, cursor_col):
    middle = _buffer[cursor_row-1]
    rows = [middle[cursor_col:]] + _buffer[cursor_row:]

    row_offset = len(_buffer) - len(rows) + 1
    col_offset = 1 # This must be updated for the first row

    open_brackets = 1 # We have one open from the start
    for r in range(len(rows)):
        for c in range(len(rows[r])):
            char = rows[r][c]
            if char in OPENING_BRACKETS:
                open_brackets += 1
            elif char in CLOSING_BRACKETS:
                open_brackets -= 1
                if open_brackets == 0:
                    if r == 0:
                        col_offset = len(middle[:cursor_col+1])
                    return (r + row_offset, c + col_offset)
   
    return None # No match found
