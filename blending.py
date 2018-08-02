from collections.abc import Hashable
from operator import itemgetter

from notes import pitch_class
from sets import relative_intervals
from chords import Chord


class Axiom(Hashable, int):

    def __hash__(self):
        return hash((
            type(self),
            int.__hash__(self)
        ))

    def __repr__(self):
        return '{}({})'.format(
            type(self).__name__,
            int(self)
        )

class AbsNote(Axiom):
    pass

class RelNote(Axiom):
    pass


def get_chord_spec(notes):
    chord = Chord.classify_uniquely(notes)
    return {
        *map(AbsNote, chord),
        *map(RelNote, relative_intervals(chord, chord.root))
    }

def get_generalization_path(spec, generic_space):
    signifying_axioms = set.difference(spec, generic_space)
    rank = rank_axiom_salience(signifying_axioms)
    # TODO: account for deviations
    return sorted(signifying_axioms, key=lambda axiom: rank[axiom])

def rank_axiom_salience(axioms):
    ranked = {}
    for axiom in axioms:
        # TODO: do this programmatically
        rank = int(
            input(f'Input salience for: {repr(axiom)} \n')
        )
        ranked[axiom] = rank
    return ranked

def generalized(spec, generalization_path, prefix):
    return {
        axiom for axiom in spec if axiom not in generalization_path[:prefix]
    }

def check_for_consistency(blendoid):
    forbidden = (
        {RelNote(3), RelNote(4)},
        {RelNote(1)},
        {RelNote(6), RelNote(7)},
    )
    axioms = get_chord_spec(blendoid)
    return not any(subset <= axioms for subset in forbidden)

def blend_chords(pc1, pc2):

    spec1 = get_chord_spec(pc1)
    spec2 = get_chord_spec(pc2)

    generic_space = set.intersection(spec1, spec2)

    path1 = get_generalization_path(spec1, generic_space)
    path2 = get_generalization_path(spec2, generic_space)
    
    solutions = []

    for i, _ in enumerate(path1):
        for j, _ in enumerate(path2):
            
            colimit = set.union(
                generalized(spec1, path1, i),
                generalized(spec2, path2, j)
            )

            deduced  = Chord.classify_uniquely(
                pitch_class(axiom) for axiom in colimit if type(axiom) is AbsNote
            )

            blendoid = {
                *deduced,
                *(pitch_class(axiom + deduced.root) for axiom in colimit if type(axiom) is RelNote)
            }

            if check_for_consistency(blendoid):
                # TODO: account for deviations from priority ordering
                cost = max(i, j) ** 2 + min(i, j)
                solutions.append((blendoid, cost))

    return min(
        solutions,
        key=itemgetter(1)
    )[0]
