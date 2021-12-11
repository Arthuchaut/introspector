from typing import Callable
from introspector.decorator import strict


class TestDecorator:
    def test_strict(self) -> None:
        expected_ret: float = 3.14

        def lambda_func(
            a: int,
            b: float | str,
            d: list[int],
            c: str = None,
        ) -> float:
            return expected_ret

        decorator: Callable[
            [int, float | str, list[int], str], float
        ] = strict(lambda_func)

        ret: float = decorator(2, 'a', [1, 2, 3])
        assert ret == expected_ret
