import sys

v = sys.version_info

if v >= (3, 8):
    from typing import Literal, Protocol
    from importlib.metadata import PackageNotFoundError, version
else:
    from typing_extensions import Literal, Protocol
    from importlib_metadata import PackageNotFoundError, version

if v >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum
