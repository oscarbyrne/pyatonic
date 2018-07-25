from itertools import (
    starmap,
    combinations_with_replacement,
)
from fractions import Fraction


chromatic_cardinality = 12
consonance_vector = (1,0,0,1,1,1,0,1,1,1,0,0)
chromatic_set = set(
    range(chromatic_cardinality)
)


# Types

def unordered_pitch_class_set(pitches):
    return set(
        p % chromatic_cardinality for p in pitches
    )

def ordered_pitch_class_set(pitches):
    return sorted(
        unordered_pitch_class_set(pitches)
    )

def directed_pitch_interval_class(pitch1, pitch2):
    return (pitch2 - pitch1) % chromatic_cardinality


# Unordered PCS transforms

def inversion(pitches, n=chromatic_cardinality):
    return type(pitches)(
        n - p for p in pitches
    )

def transposition(pitches, n):
    return type(pitches)(
        p + n for p in pitches
    )


#  Ordered PCS transforms

def rotation(pitches, n):
    return tuple(
        pitches[n:] + pitches[:n]
    )

def stepwise_intervals(pitches):
    return tuple(starmap(
        directed_pitch_interval_class,
        zip(
            pitches,
            rotation(pitches, 1)
        )
    ))

def scale_intervals(pitches, root=None):
    if root is None:
        root = pitches[0]
    return ordered_pitch_class_set(
        transposition(pitches, -root)
    )




def normal_order(pitches):
    pcs = ordered_pitch_class_set(pitches)
    ics = stepwise_intervals(pcs)
    candidates = [
        rotation(pcs, i + 1)
        for i, x in enumerate(ics) if x == max(ics)
    ]
    return min(
        candidates,
        key=scale_intervals
    )

def prime_form(pitches):
    nf1 = normal_order(pitches)
    nf2 = normal_order(inversion(nf1))
    return min(
        nf1, nf2,
        key=scale_intervals
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

def idiomatically_consonant_pitch_classes(pitches, select_from=chromatic_set):
    pcs = unordered_pitch_class_set(pitches)
    return {
        pitch for pitch in select_from
        if idiomatic_consonance(
            set.union(pcs, {pitch})
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

    gcts = zip(base_sets, extensions)

    for i, gct in enumerate(gcts):
        base, exts = gct
        root = base[0]
        base = scale_intervals(base, root)
        exts = scale_intervals(exts, root)
        gcts[i] = (root, base, exts)

    return tuple(gcts)







