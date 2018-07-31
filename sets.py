from itertools import (
    tee,
    starmap,
    islice,
    cycle,
    chain,
)
from functools import partial

from assumptions import chromatic_cardinality
from notes import (
    directed_pitch_interval_class,
    pitch_class,
)


def inverted(notes, n=chromatic_cardinality):
    return (n - note for note in notes)

def transposed(notes, n):
    return (note + n for note in notes)

def rotated(notes, n):
    return tuple(chain(
        islice(notes, n, None),
        islice(notes, n)
    ))

def stepwise_intervals(notes):
    a, b = tee(notes)
    b = islice(cycle(b), 1, None)
    return tuple(starmap(
        directed_pitch_interval_class,
        zip(a, b)
    ))

def relative_intervals(notes, root=None):
    if root is None:
        notes, copy = tee(notes)
        root = next(copy, None)
    return tuple(map(
        partial(directed_pitch_interval_class, root),
        notes
    ))

def normal_order(notes):
    if not notes:
        return tuple()
    pcs = sorted(set(
        map(pitch_class, notes)
    ))
    ics = stepwise_intervals(pcs)
    candidates = tuple(
        rotated(pcs, n + 1)
        for n, ic in enumerate(ics) if ic == max(ics)
    )
    return min(
        candidates,
        key=relative_intervals
    )

def prime_form(notes):
    if not notes:
        return tuple()
    nf1 = normal_order(notes)
    nf2 = normal_order(inverted(nf1))
    return min(
        nf1, nf2,
        key=relative_intervals
    )
