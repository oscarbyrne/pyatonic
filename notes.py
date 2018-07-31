from assumptions import chromatic_cardinality


chromatic_set = frozenset(range(chromatic_cardinality))

def directed_pitch_interval_class(note1, note2):
    return (note2 - note1) % chromatic_cardinality

def pitch_class(note):
    return note % chromatic_cardinality
