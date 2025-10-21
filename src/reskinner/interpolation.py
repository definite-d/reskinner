from typing import Dict
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

from colour import Color


def _clamp(v: float):
    return min(max(v, 0), 1)


class InterpolationFormula(Protocol):
    def __call__(self, start: float, end: float, progress: float) -> float: ...


class InterpolationMethod(Protocol):
    def __call__(self, start: Color, end: Color, progress: float) -> Color: ...


def _lerp(start: float, end: float, progress: float):
    return start + ((end - start) * progress)


def _hue_swap(start: float, end: float, progress: float):
    if start > end:
        start, end = end, start
        progress = 1 - progress
    diff = end - start
    if diff > 0.5:
        return ((start + 1) + progress * (end - (start + 1))) % 1
    else:
        return start + progress * diff


def _interpolate(
    start: Color,
    end: Color,
    progress: float,
    components_and_methods: Dict[str, InterpolationFormula],
):
    if progress == 1:
        return end
    elif progress == 0:
        return start
    values = {
        component: _clamp(
            method(
                getattr(start, component),
                getattr(end, component),
                progress,
            )
        )
        for component, method in components_and_methods.items()
    }
    return Color(**values)


def rgb(start: Color, end: Color, progress: float):
    return _interpolate(
        start,
        end,
        progress,
        {
            "red": _lerp,
            "green": _lerp,
            "blue": _lerp,
        },
    )


def hue(start: Color, end: Color, progress: float):
    return _interpolate(
        start,
        end,
        progress,
        {
            "hue": _lerp,
            "saturation": _lerp,
            "luminance": _lerp,
        },
    )


def hsl(start: Color, end: Color, progress: float):
    return _interpolate(
        start,
        end,
        progress,
        {
            "hue": _hue_swap,
            "saturation": _lerp,
            "luminance": _lerp,
        },
    )


INTERPOLATION_MODES = {
    "hsl": hsl,
    "hue": hue,
    "rgb": rgb,
}
