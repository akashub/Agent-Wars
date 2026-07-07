def full_justify(words, max_width):
    """Format `words` into lines of EXACTLY `max_width` characters, fully justified.
      - Pack as many words per line as fit (words joined by >=1 space).
      - Distribute spaces as evenly as possible; if spaces don't divide evenly, the
        LEFT gaps get one extra space each.
      - A line with a single word, and the LAST line, are LEFT-justified: words
        separated by a single space, then padded with trailing spaces to max_width.
    Return the list of justified lines (each len == max_width).
    """
    raise NotImplementedError
