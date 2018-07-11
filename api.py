from itertools import (
    starmap,
    combinations
)

from config import cardinality


def pitch_class(pitch):
    return pitch % cardinality

def pitch_interval(pitch1, pitch2):
    return pitch2 - pitch1

def directed_pitch_interval_class(pitch1, pitch2):
    return pitch_interval(pitch1, pitch2) % cardinality

def undirected_pitch_interval_class(pitch1, pitch2):
    return min(
        directed_pitch_interval_class(pitch1, pitch2),
        directed_pitch_interval_class(pitch2, pitch1)
    )

def unordered_pitch_class_set(pitches):
    return set(
        map(pitch_class, pitches)
    )

def ordered_pitch_class_set(pitches):
    return sorted(
        unordered_pitch_class_set(pitches)
    )

def transposition(n, pitches):
    return type(pitches)(
        pitch_class(pitch + n) for pitch in pitches
    )

def inversion(pitches):
    return type(pitches)(
        cardinality - pitch for pitch in pitches
    )

def rotation(n, pitches):
    return tuple(
        pitches[n:] + pitches[:n]
    )

def stepwise_intervals(pitches):
    return tuple(starmap(
        directed_pitch_interval_class,
        zip(
            pitches,
            rotation(1, pitches)
        )
    ))

def degree_intervals(pitches):
    return tuple(starmap(
        directed_pitch_interval_class,
        ((pitches[0], p) for p in pitches)
    ))

def normal_order(pitches):
    pcs = ordered_pitch_class_set(pitches)
    ics = stepwise_intervals(pcs)
    candidates = [
        rotation(i + 1, pcs)
        for i, x in enumerate(ics) if x == max(ics)
    ]
    return min(
        candidates,
        key=degree_intervals
    )

def normal_form(pitches):
    pitches = normal_order(pitches)
    return degree_intervals(pitches)

def prime_form(pitches):
    nf1 = normal_form(pitches)
    nf2 = normal_form(inversion(nf1))
    return min(nf1, nf2, key=sum)

def interval_vector(pitches):
    ics = tuple(starmap(
        undirected_pitch_interval_class,
        combinations(pitches, 2)
    ))
    return tuple(
        ics.count(i) for i in range(1, 1 + cardinality / 2)
    )

def is_deep_scale(pitches):
    iv = interval_vector(pitches)
    return len(set(iv)) == len(iv) 
