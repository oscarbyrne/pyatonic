from collections.abc import Sequence
from itertools import (
    combinations_with_replacement,
    chain,
)
from fractions import Fraction
from functools import partial

from assumptions import (
    consonance_vector,
    chromatic_cardinality,
)
from notes import (
    directed_pitch_interval_class,
    chromatic_set,
    pitch_class,
)
from sets import (
    normal_order,
    relative_intervals,
    transposed,
)


def internal_consonance(notes):
    pairs = tuple(combinations_with_replacement(notes, 2))
    return Fraction(
        sum(
            consonance_vector[
                directed_pitch_interval_class(*pair)
            ] for pair in pairs
        ),
        len(pairs)
    )

def consonant_to(notes, select_from=chromatic_set):
    return {
        pitch for pitch in select_from
        if internal_consonance({pitch, *notes}) == 1
    }

def consonant_subsets(notes):
    graph = {
        pitch: consonant_to({pitch}, notes)
        for pitch in notes
    }

    consonant_sets = set()

    def visit_node(node, visited):
        visited.add(node)
        consonant_sets.add(frozenset(visited))
        connected = set.union(
            *(graph[leaf] for leaf in visited)
        )
        consonant = consonant_to(
            visited,
            connected
        )
        candidates = consonant - visited
        for next in candidates:
            visit_node(next, visited.copy())

    for start in graph:
        visit_node(start, set())

    return consonant_sets


class Chord(Sequence):

    @classmethod
    def classify(cls, notes):

        notes = set(
            map(
                pitch_class,
                notes
            )
        )
        
        consonant_sets = consonant_subsets(notes)

        max_length = len(
            max(consonant_sets, key=len)
        )

        base_sets = tuple(
            normal_order(pcs) for pcs in consonant_sets if len(pcs) == max_length
        )

        gcts = []

        for base in base_sets:
            root = base[0]
            exts = normal_order(set(notes) - set(base))
            base = relative_intervals(base, root)
            exts = relative_intervals(exts, root)
            gcts.append(
                cls(root, base, exts)
            )

        return tuple(gcts)

    @classmethod
    def classify_uniquely(cls, notes):
        # TODO: full implementation
        return cls.classify(notes)[0]

    def __init__(self, root, base, extensions):
        self.root = root
        self.base = tuple(base)
        self.extensions = tuple(extensions)

    @property
    def notes(self):
        return tuple(map(
            pitch_class,
            chain(
                transposed(self.base, self.root),
                transposed(self.extensions, self.root)
            )
        ))

    def __getitem__(self, i):
        return self.notes[i]

    def __len__(self):
        return len(self.notes)

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            ', '.join((
                repr(self.root),
                repr(self.base),
                repr(self.extensions)
            ))
        )
