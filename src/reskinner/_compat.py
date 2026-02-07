import sys

v = sys.version_info

if v >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
    from typing import Literal, Protocol, Type
else:
    from importlib_metadata import PackageNotFoundError, version
    from typing_extensions import Literal, Protocol, Type

if v >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum

__all__ = ["PackageNotFoundError", "version", "Literal", "Protocol", "StrEnum", "Type"]
