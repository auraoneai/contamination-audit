__all__ = ["run"]

def __getattr__(name):
    if name == "run":
        from .cli import run
        return run
    raise AttributeError(name)
