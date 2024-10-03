from functools import wraps
from typing import Type


def transform_exception(fr0m: Type[Exception], to: Type[Exception]):
    """Useful, e.g. for view methods to transform your internal logic exception to validation exception."""

    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except fr0m as ex:
                raise to(ex)

        return wrapped

    return decorator
