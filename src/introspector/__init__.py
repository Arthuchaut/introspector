from typing import Any, Callable
from .strict import Strict


def strict(*args: Any, **kwargs: Any) -> None:
    def call(fx: Callable[[Any], Any]) -> Callable[[Any], Any]:
        sct: Strict = Strict(*args, **kwargs)
        return sct(fx)

    if args and callable(args[0]):
        sct: Strict = Strict()
        return sct(args[0])
    else:
        return call
