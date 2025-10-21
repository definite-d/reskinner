try:
    from importlib.metadata import PackageNotFoundError, version
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("reskinner")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
