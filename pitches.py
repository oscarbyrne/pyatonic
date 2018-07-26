from config import chromatic_cardinality


def directed_pitch_interval_class(pitch1, pitch2):
    return (pitch2 - pitch1) % chromatic_cardinality

def undirected_pitch_interval_class(pitch1, pitch2):
    return min(
        directed_pitch_interval_class(pitch1, pitch2),
        directed_pitch_interval_class(pitch2, pitch1)
    )

def pitch_class(pitch):
    return pitch % chromatic_cardinality

def inverted(pitch, n=chromatic_cardinality):
    return n - pitch

def transposed(pitch, n):
    return pitch + n
