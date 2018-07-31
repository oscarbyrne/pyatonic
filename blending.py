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


def get_chord_spec(notes, root):
    return {
        *map(AbsNote, notes),
        *map(RelNote, relative_intervals(notes, root))
    }

def check_for_consonance(axioms):
    forbidden = (
        {RelNote(3), RelNote(4)},
        {RelNote(1)},
        {RelNote(6), RelNote(7)},
    )
    return not any(subset <= axioms for subset in forbidden)

def rank_axiom_salience(axioms):
    ranked = {}
    for axiom in axioms:
        # TODO: do this programmatically
        rank = int(
            input(f'Input salience for: {repr(axiom)} \n')
        )
        ranked[axiom] = rank
    return ranked

def get_generalization_path(spec, generic_space):
    signifying_axioms = set.difference(spec, generic_space)
    rank = rank_axiom_salience(signifying_axioms)
    # TODO: account for deviations
    return sorted(signifying_axioms, key=lambda axiom: rank[axiom])

def generalized(spec, generalization_path, prefix):
    return {
        axiom for axiom in spec if axiom not in generalization_path[:prefix]
    }

def blend_chords(pc1, pc2):
    chord1 = Chord.classify_uniquely(pc1)
    chord2 = Chord.classify_uniquely(pc2)

    spec1 = get_chord_spec(chord1, chord1.root)
    spec2 = get_chord_spec(chord2, chord2.root)

    generic_space = set.intersection(spec1, spec2)

    path1 = get_generalization_path(spec1, generic_space)
    path2 = get_generalization_path(spec2, generic_space)
    
    solutions = []

    for i, _ in enumerate(path1):
        for j, _ in enumerate(path2):

            generalized1 = generalized(spec1, path1, i)
            generalized2 = generalized(spec2, path2, j)
            
            # TODO: is this colimit operator correct?
            colimit = set.union(generalized1, generalized2)

            deduced  = Chord.classify_uniquely(
                pitch_class(axiom) for axiom in colimit if type(axiom) is AbsNote
            )

            additional = (
                pitch_class(axiom + deduced.root) for axiom in colimit if type(axiom) is RelNote
            )

            completed = Chord.classify_uniquely(
                {*deduced, *additional}
            )

            spec = get_chord_spec(
                completed,
                completed.root
            )

            if deduced.root == completed.root and check_for_consonance(spec):
                # TODO: account for deviations from priority ordering
                cost = max(i, j) ** 2 + min(i, j)
                solutions.append((completed, cost))

    return min(
        solutions,
        key=itemgetter(1)
    )[0]
