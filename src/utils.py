# Taken from https://stackoverflow.com/a/26856771
def hsv_to_rgb(h: float, s: int, v: int):
    """
    Convert an HSV color value to an RGB color value.
    Assumes h, s, and v are in the range [0, 1] and h is a float.
    Returns a tuple of (r, g, b) values in the range [0, 255].
    """
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)