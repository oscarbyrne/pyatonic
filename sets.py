from itertools import (
    tee,
    starmap,
    islice,
    cycle,
    chain,
)
from functools import partial

from pitches import (
    directed_pitch_interval_class,
    inverted,
    pitch_class,
)


def rotated(pitches, n):
    return tuple(chain(
        islice(pitches, n, None),
        islice(pitches, n)
    ))

def stepwise_intervals(pitches):
    a, b = tee(pitches)
    b = islice(cycle(b), 1, None)
    return tuple(starmap(
        directed_pitch_interval_class,
        zip(a, b)
    ))

def relative_intervals(pitches, root=None):
    if root is None:
        pitches, copy = tee(pitches)
        root = next(copy)
    return tuple(map(
        partial(directed_pitch_interval_class, root),
        pitches
    ))

def normal_order(pitches):
    pcs = sorted(set(
        map(pitch_class, pitches)
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

def prime_form(pitches):
    nf1 = normal_order(pitches)
    nf2 = normal_order(map(inverted, nf1))
    return min(
        nf1, nf2,
        key=relative_intervals
    )