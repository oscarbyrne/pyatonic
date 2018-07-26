from itertools import (
    combinations_with_replacement,
)
from fractions import Fraction

from config import (
    chromatic_cardinality,
    consonance_vector,
)
from pitches import directed_pitch_interval_class
from sets import (
    normal_order,
    relative_intervals
)


def consonance(pitches):
    pairs = tuple(combinations_with_replacement(pitches, 2))
    return Fraction(
        sum(
            consonance_vector[
                directed_pitch_interval_class(*pair)
            ] for pair in pairs
        ),
        len(pairs)
    )

def consonant_pitch_classes(pitches, select_from=None):
    if select_from is None:
        select_from = range(chromatic_cardinality)
    pitches = set(pitches)
    return {
        pitch for pitch in select_from
        if consonance(
            set.union(pitches, {pitch})
        ) == 1
    }

def consonant_subsets(pitches):
    graph = {
        pitch: consonant_pitch_classes(
            {pitch},
            select_from=pitches
        )
        for pitch in pitches
    }

    consonant_sets = set()

    def visit_node(node, visited):
        visited.add(node)
        consonant_sets.add(frozenset(visited))
        consonant = consonant_pitch_classes(
            visited,
            select_from=set.union(
                *(graph[leaf] for leaf in visited)
            )
        )
        for next in consonant - visited:
            visit_node(next, visited.copy())

    for start in graph:
        visit_node(start, set())

    return consonant_sets


# TODO: probably make this a class so we can iterate over pitches
def general_chord_type(pitches):
    
    consonant_sets = consonant_subsets(pitches)

    max_length = len(
        max(consonant_sets, key=len)
    )
    
    base_sets = tuple(
        normal_order(pcs) for pcs in consonant_sets if len(pcs) == max_length
    )

    extensions = tuple(
        normal_order(set(pitches) - set(base_set)) for base_set in base_sets
    )

    gcts = list(
        zip(base_sets, extensions)
    )

    for i, gct in enumerate(gcts):
        base, exts = gct
        root = base[0]
        base = relative_intervals(base, root)
        exts = relative_intervals(exts, root)
        gcts[i] = (root, base, exts)

    return tuple(gcts)