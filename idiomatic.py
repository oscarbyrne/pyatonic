from itertools import combinations_with_replacement
from fractions import Fraction

from config import (
    consonance_vector,
    chromatic_cardinality,
    chromatic_set,
)
from pitches import directed_pitch_interval_class
from sets import (
    normal_order,
    relative_intervals
)


def internal_consonance(pitches):
    pairs = tuple(combinations_with_replacement(pitches, 2))
    return Fraction(
        sum(
            consonance_vector[
                directed_pitch_interval_class(*pair)
            ] for pair in pairs
        ),
        len(pairs)
    )

def consonant_to(pitches, select_from=chromatic_set): 
    return {
        pitch for pitch in select_from
        if internal_consonance({pitch, *pitches}) == 1
    }

def consonant_subsets(pitches):
    graph = {
        pitch: consonant_to({pitch}, pitches)
        for pitch in pitches
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

# TODO: probably make this a class so we can iterate over pitches
def general_chord_type(pitches):
    
    consonant_sets = consonant_subsets(pitches)

    max_length = len(
        max(consonant_sets, key=len)
    )
    
    base_sets = tuple(
        normal_order(pcs) for pcs in consonant_sets if len(pcs) == max_length
    )

    gcts = []

    for base in base_sets:
        root = base[0]
        exts = normal_order(set(pitches) - set(base))
        base = relative_intervals(base, root)
        exts = relative_intervals(exts, root)
        gcts.append(
            (root, base, exts)
        )

    return tuple(gcts)