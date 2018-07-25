from collections import (
    Sized,
    Iterable,
    Container,
    Sequence,
)

from abc import (
    ABCMeta,
    abstractproperty
)

class PCS(Sized, Iterable, Container):

    __metaclass__ = ABCMeta

    @abstractproperty
    def pcs(self):
        raise NotImplementedError

    def __contains__(self, other):
        return other in self.pcs

    def __iter__(self):
        return iter(self.pcs)

    def __len__(self):
        return len(self.pcs)


class UPSLib():
    
    def get_ordered(ps):
        return OPCS(ps)


class OPSLib():

    def get_unordered(ps):
        return UPCS(ps)


class UPCS(PCS, UPSLib):

    def __init__(self, pcs):
        self._pcs = set(pcs)

    @property
    def pcs(self):
        return self._pcs


class OPCS(PCS, Sequence, UPSLib, OPSLib):

    def __init__(self, pcs):
        self._pcs = tuple(pcs)

    @property
    def pcs(self):
        return self._pcs

    def __getitem__(self, i):
        return self.pcs[i]


class GCT(OPCS):

    def __init__(self, root, base, extensions):
        self.root = root
        self.base = base
        self.extensions = extensions

    @property
    def pcs(self):
        # TODO
        return (1,2,3)






