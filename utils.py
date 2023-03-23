def hsv_to_rgb(h, s, v):
    """
    Convert an HSV color value to an RGB color value.
    Assumes h, s, and v are in the range [0, 1].
    Returns a tuple of (r, g, b) values in the range [0, 1].
    """
    if s == 0:
        r = g = b = v
    else:
        h *= 6  # sector 0 to 5
        i = int(h)
        f = h - i  # fractional part of h
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
    return r, g, b
