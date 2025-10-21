from math import cos, pi, sin, sqrt
from typing import Callable, Dict, Optional, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

c1 = 1.70158
c2 = c1 * 1.525
c3 = c1 + 1
c4 = (2 * pi) / 3
c5 = (2 * pi) / 4.5  # Needed for elastic easing


def _ease_out_bounce(x: float) -> float:
    n1 = 7.5625
    d1 = 2.75

    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375


def _ease_in_bounce(x: float) -> float:
    return 1 - _ease_out_bounce(1 - x)


def _ease_in_out_bounce(x: float) -> float:
    if x < 0.5:
        return (1 - _ease_out_bounce(1 - 2 * x)) / 2
    else:
        return (1 + _ease_out_bounce(2 * x - 1)) / 2


EASING_FUNCTIONS: Dict[str, Callable[[float], float]] = {
    "ease_in_sine": lambda x: 1 - cos((x * pi) / 2),
    "ease_out_sine": lambda x: sin((x * pi) / 2),
    "ease_in_out_sine": lambda x: -(cos(pi * x) - 1) / 2,
    "ease_in_quad": lambda x: x**2,
    "ease_out_quad": lambda x: 1 - (1 - x) ** 2,
    "ease_in_out_quad": lambda x: (
        2 * x * x if x < 0.5 else 1 - ((-2 * x + 2) ** 2) / 2
    ),
    "ease_in_cubic": lambda x: x**3,
    "ease_out_cubic": lambda x: 1 - (1 - x) ** 3,
    "ease_in_out_cubic": lambda x: (
        4 * x**3 if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2
    ),
    "ease_in_quart": lambda x: x**4,
    "ease_out_quart": lambda x: 1 - (1 - x) ** 4,
    "ease_in_out_quart": lambda x: (
        8 * x**4 if x < 0.5 else 1 - ((-2 * x + 2) ** 4) / 2
    ),
    "ease_in_quint": lambda x: x**5,
    "ease_out_quint": lambda x: 1 - (1 - x) ** 5,
    "ease_in_out_quint": lambda x: (
        16 * x**5 if x < 0.5 else 1 - ((-2 * x + 2) ** 5) / 2
    ),
    "ease_in_expo": lambda x: 0 if x == 0 else 2 ** (10 * x - 10),
    "ease_out_expo": lambda x: 1 if x == 1 else 1 - 2 ** (-10 * x),
    "ease_in_out_expo": lambda x: (
        x
        if x in (0, 1)
        else (2 ** (20 * x - 10) / 2 if x < 0.5 else (2 - 2 ** (-20 * x + 10)) / 2)
    ),
    "ease_in_circ": lambda x: 1 - sqrt(1 - x**2),
    "ease_out_circ": lambda x: sqrt(1 - (x - 1) ** 2),
    "ease_in_out_circ": lambda x: (
        (1 - sqrt(1 - (2 * x) ** 2)) / 2
        if x < 0.5
        else (sqrt(1 - (-2 * x + 2) ** 2) + 1) / 2
    ),
    "ease_in_back": lambda x: c3 * x**3 - c1 * x**2,
    "ease_out_back": lambda x: 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2,
    "ease_in_out_back": lambda x: (
        ((2 * x) ** 2 * ((c2 + 1) * 2 * x - c2)) / 2
        if x < 0.5
        else ((2 * x - 2) ** 2 * ((c2 + 1) * (2 * x - 2) + c2) + 2) / 2
    ),
    "ease_in_elastic": lambda x: (
        x if x in (0, 1) else -(2 ** (10 * x - 10)) * sin((x * 10 - 10.75) * c4)
    ),
    "ease_out_elastic": lambda x: (
        x if x in (0, 1) else 2 ** (-10 * x) * sin((x * 10 - 0.75) * c4) + 1
    ),
    "ease_in_out_elastic": lambda x: (
        x
        if x in (0, 1)
        else (
            -(2 ** (20 * x - 10) * sin((20 * x - 11.125) * c5)) / 2
            if x < 0.5
            else 2 ** (-20 * x + 10) * sin((20 * x - 11.125) * c5) / 2 + 1
        )
    ),
    "ease_in_bounce": _ease_in_bounce,
    "ease_out_bounce": _ease_out_bounce,
    "ease_in_out_bounce": _ease_in_out_bounce,
}


EasingName = Literal[
    "ease_in_sine",
    "ease_out_sine",
    "ease_in_out_sine",
    "ease_in_quad",
    "ease_out_quad",
    "ease_in_out_quad",
    "ease_in_cubic",
    "ease_out_cubic",
    "ease_in_out_cubic",
    "ease_in_quart",
    "ease_out_quart",
    "ease_in_out_quart",
    "ease_in_quint",
    "ease_out_quint",
    "ease_in_out_quint",
    "ease_in_expo",
    "ease_out_expo",
    "ease_in_out_expo",
    "ease_in_circ",
    "ease_out_circ",
    "ease_in_out_circ",
    "ease_in_back",
    "ease_out_back",
    "ease_in_out_back",
    "ease_in_elastic",
    "ease_out_elastic",
    "ease_in_out_elastic",
    "ease_in_bounce",
    "ease_out_bounce",
    "ease_in_out_bounce",
]


def ease(
    progress: float,
    function: Optional[Union[EasingName, Callable[[float], float]]] = None,
) -> float:
    if not 0 <= progress <= 1:
        raise ValueError("Progress must be between 0 and 1.")

    if function is None:
        return progress

    if callable(function):
        return function(progress)

    easing_func = EASING_FUNCTIONS.get(function)
    if easing_func is None:
        raise ValueError(f"Unknown easing function: {function}")

    return easing_func(progress)
