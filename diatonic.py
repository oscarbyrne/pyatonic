from collections.abc import Sequence
from math import floor

from assumptions import (
    chromatic_cardinality,
    diatonic_cardinality,
)
from notes import chromatic_set


def maximally_even_set(c, d, a=0):
    return tuple(
        floor((k * c + a) / d) for k in range(d)
    )

class DiatonicSubset(Sequence):

    @classmethod
    def from_cardinality(cls, basis, cardinality, mode):
        return cls(
            basis,
            maximally_even_set(len(basis), cardinality, mode)
        )

    def __init__(self, basis, mapping):
        self.basis = tuple(basis)
        self.mapping = tuple(mapping)

    @property
    def notes(self):
        return tuple(
            self.basis[i] for i in self.mapping
        )

    def __getitem__(self, i):
        return self.notes[i]

    def __len__(self):
        return len(self.notes)

    def __repr__(self):
        return '{}({},{})'.format(
            type(self).__name__,
            self.basis,
            self.mapping
        )

diatonic_sets = tuple(
    DiatonicSubset.from_cardinality(
        sorted(chromatic_set),
        diatonic_cardinality,
        mode
    ) for mode in range(chromatic_cardinality)
)
