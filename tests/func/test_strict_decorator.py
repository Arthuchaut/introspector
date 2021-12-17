from typing import Any, Callable
import pytest
from src.introspector.strict import Strict
from src.introspector import strict


class TestStrictClassDecorator:
    class Fake:
        ...

    @pytest.mark.parametrize(
        'func_name, args, kwargs, expected_ret, throwable',
        [
            ('_lambda_func_1', (2, 'a', [1, 2, 3]), {}, 3.14, None),
            ('_lambda_func_4', (2, 'a'), {'d': [1, 2]}, 3.14, None),
            ('_lambda_func_5', (Fake(), 3.14), {'d': [1, 2]}, 3.14, None),
            ('_lambda_func_6', (2, 4, [1, 2, 3]), {}, 3.14, None),
            ('_lambda_func_1', (2, 4, [1, 2, 3]), {}, 3.14, TypeError),
            ('_lambda_func_2', (2, 'a', [1, 2, 3]), {}, None, TypeError),
            ('_lambda_func_3', (2, 'a'), {}, None, TypeError),
        ],
    )
    def test_decorator(
        self,
        func_name: str,
        args: Any,
        kwargs: Any,
        expected_ret: Any,
        throwable: TypeError | None,
    ) -> None:
        func: Callable[[Any], Any] = getattr(self, func_name)

        if throwable:
            with pytest.raises(throwable):
                func(*args, **kwargs)
        else:
            ret: Any = func(*args, **kwargs)
            assert ret == expected_ret

    @Strict()
    def _lambda_func_1(
        self,
        a: int,
        b: float | str,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14

    @Strict()
    def _lambda_func_2(
        self,
        a: int,
        b: float | str,
        d: list[int],
        c: str = None,
    ) -> float:
        return 'not a float'

    @Strict()
    def _lambda_func_3(
        self,
        a: int,
        b,
    ) -> float:
        return 3.14

    @Strict()
    def _lambda_func_4(
        self,
        a: int,
        b: float | str,
        *,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14

    @Strict()
    def _lambda_func_5(
        self,
        a: Fake,
        b: int | float,
        *,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14

    @Strict(ignore=['b'])
    def _lambda_func_6(
        self,
        a: int,
        b: float | str,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14


class TestStrictFunctionDecorator:
    class Fake:
        ...

    @pytest.mark.parametrize(
        'func_name, args, kwargs, expected_ret, throwable',
        [
            ('_lambda_func_1', (2, 'a', [1, 2, 3]), {}, 3.14, None),
            ('_lambda_func_4', (2, 'a'), {'d': [1, 2]}, 3.14, None),
            ('_lambda_func_5', (Fake(), 3.14), {'d': [1, 2]}, 3.14, None),
            ('_lambda_func_6', (2, 4, [1, 2, 3]), {}, 3.14, None),
            ('_lambda_func_1', (2, 4, [1, 2, 3]), {}, 3.14, TypeError),
            ('_lambda_func_2', (2, 'a', [1, 2, 3]), {}, None, TypeError),
            ('_lambda_func_3', (2, 'a'), {}, None, TypeError),
        ],
    )
    def test_decorator(
        self,
        func_name: str,
        args: Any,
        kwargs: Any,
        expected_ret: Any,
        throwable: TypeError | None,
    ) -> None:
        func: Callable[[Any], Any] = getattr(self, func_name)

        if throwable:
            with pytest.raises(throwable):
                func(*args, **kwargs)
        else:
            ret: Any = func(*args, **kwargs)
            assert ret == expected_ret

    @strict
    def _lambda_func_1(
        self,
        a: int,
        b: float | str,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14

    @strict
    def _lambda_func_2(
        self,
        a: int,
        b: float | str,
        d: list[int],
        c: str = None,
    ) -> float:
        return 'not a float'

    @strict
    def _lambda_func_3(
        self,
        a: int,
        b,
    ) -> float:
        return 3.14

    @strict
    def _lambda_func_4(
        self,
        a: int,
        b: float | str,
        *,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14

    @strict
    def _lambda_func_5(
        self,
        a: Fake,
        b: int | float,
        *,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14

    @strict(ignore=['b'])
    def _lambda_func_6(
        self,
        a: int,
        b: float | str,
        d: list[int],
        c: str = None,
    ) -> float:
        return 3.14
