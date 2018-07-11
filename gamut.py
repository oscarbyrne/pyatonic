from itertools import (
    chain,
    combinations,
)

from api import (
    prime_form,
    is_deep_scale,
)

from config import cardinality


pc = set(
    range(cardinality)
)

sc = set(
    chain.from_iterable(
        iter(
            prime_form(s)
            for s in combinations(pc, n)
        ) for n in range(2, len(pc))
    )
)

deep_scales = set(
    filter(
        is_deep_scale,
        sc
    )
)