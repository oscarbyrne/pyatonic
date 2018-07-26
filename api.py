from itertools import (
    tee,
    starmap,
    islice,
    cycle,
    chain,
    combinations_with_replacement,
)
from functools import partial
from fractions import Fraction


chromatic_cardinality = 12
consonance_vector = (1,0,0,1,1,1,0,1,1,1,0,0)



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



def idiomatic_consonance(pitches):
    pairs = tuple(combinations_with_replacement(pitches, 2))
    return Fraction(
        sum(
            consonance_vector[
                directed_pitch_interval_class(*pair)
            ] for pair in pairs
        ),
        len(pairs)
    )

def idiomatically_consonant_pitch_classes(pitches, select_from=None):
    if select_from is None:
        select_from = range(chromatic_cardinality)
    pitches = set(pitches)
    return {
        pitch for pitch in select_from
        if idiomatic_consonance(
            set.union(pitches, {pitch})
        ) == 1
    }

def idiomatically_consonant_subsets(pitches):
    graph = {
        pitch: idiomatically_consonant_pitch_classes(
            {pitch},
            select_from=pitches
        )
        for pitch in pitches
    }

    consonant_sets = set()

    def visit_node(node, visited):
        visited.add(node)
        consonant_sets.add(frozenset(visited))
        consonant = idiomatically_consonant_pitch_classes(
            visited,
            select_from=set.union(
                *(graph[leaf] for leaf in visited)
            )
        )
        for next in consonant.difference(visited):
            visit_node(next, visited.copy())

    for start in graph:
        visit_node(start, set())

    return consonant_sets


def general_chord_type(pitches):
    
    consonant_sets = idiomatically_consonant_subsets(pitches)

    max_length = len(
        max(consonant_sets, key=len)
    )
    
    base_sets = tuple(
        normal_order(pcs) for pcs in consonant_sets if len(pcs) == max_length
    )

    extensions = tuple(
        normal_order(set(pitches) - set(base_set)) for base_set in base_sets
    )

    gcts = tuple(
        zip(base_sets, extensions)
    )

    for i, gct in enumerate(gcts):
        base, exts = gct
        root = base[0]
        base = relative_intervals(base, root)
        exts = relative_intervals(exts, root)
        gcts[i] = (root, base, exts)

    return tuple(gcts)