__all__ = ["run", "load", "select_registry"]

def __getattr__(name):
    if name == "run":
        from .cli import run
        return run
    if name == "load":
        from .cli import load
        return load
    if name == "select_registry":
        from .cli import select_registry
        return select_registry
    raise AttributeError(name)
