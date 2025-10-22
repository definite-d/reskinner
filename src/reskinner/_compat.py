import sys

v = sys.version_info

if v >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
    from typing import Literal, Protocol
else:
    from importlib_metadata import PackageNotFoundError, version
    from typing_extensions import Literal, Protocol

if v >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum
