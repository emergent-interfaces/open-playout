def extract_axb(text, default_a=None, default_b=None):
    a, delimiter, b = text.partition('x')
    if b != "":
        a = int(a)
        b = int(b)
    else:
        a = default_a
        b = default_b

    return a, b
