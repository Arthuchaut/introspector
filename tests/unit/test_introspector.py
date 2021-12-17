from typing import Any, Callable, TypeVar
import pytest
from src.introspector.introspector import Introspector


class TestIntrospector:
    T = TypeVar('T')

    @pytest.mark.parametrize(
        'type_, value, throwable',
        [
            # Primitive types tests
            (int, 200, None),
            (float, 3.14, None),
            (str, 'foo', None),
            (bool, True, None),
            (bool, False, None),
            (int, None, None),
            (int | float, 3.14, None),
            (int | float, 5, None),
            (int | float | str, 2, None),
            (int | float | str, 3.14, None),
            (int | float | str, 'a', None),
            (int, 'a', TypeError),
            (float, 3, TypeError),
            (str, 5, TypeError),
            (bool, 1, TypeError),
            (bool, 0, TypeError),
            (int | float, 'a', TypeError),
            (int | float, True, TypeError),
            (int | float | str, False, TypeError),
            # Complex types tests
            (list[int], [1, 2, 3, 4], None),
            (list[str], ['a', 'b', 'c', 'd'], None),
            (list[float], [2.4, 5.2], None),
            (list[bool], [True, False], None),
            (list[int], [1, 2, None, None], None),
            (list[int | None], [1, 2, 3, 4, None], None),
            (list[int | str | None], ['a', 4], None),
            (list[int | bool], [True, False, 4], None),
            (list[int | str], ['a', 4], None),
            (tuple[str, str], ('a', 'b'), None),
            (tuple[int, str], (4, 'b'), None),
            (tuple[float, str, bool], (3.14, 'b', True), None),
            (tuple[float, str | int, bool], (3.14, 'b', True), None),
            (tuple[float, str | int, bool], (3.14, 4, True), None),
            (set[int], {1, 2}, None),
            (set[float], {1.2, 3.14}, None),
            (set[str], {'a', 'b'}, None),
            (set[bool], {True, False}, None),
            (set[int | str], {'a', 5}, None),
            (dict[str, int], {'a': 1, 'b': 2}, None),
            (dict[str, float], {'a': 1.0, 'b': 2.0}, None),
            (dict[str, str], {'a': 'a', 'b': 'b'}, None),
            (dict[str, bool], {'a': True, 'b': False}, None),
            (dict[int, int], {1: 1, 2: 2}, None),
            (dict[int, float], {1: 1.0, 2: 2.0}, None),
            (dict[int, str], {1: 'a', 2: 'b'}, None),
            (dict[int, bool], {1: True, 2: False}, None),
            (dict[int | str, bool], {1: True, 'a': False}, None),
            (dict[int | str, bool | float], {1: True, 'a': 3.14}, None),
            (list[int], ['a', 'b', 'c', 'd'], TypeError),
            (list[str], [1, 2, 3, 4], TypeError),
            (list[float], [2, 5], TypeError),
            (list[bool], ['True', 'False'], TypeError),
            (tuple[str, str], (2, 'b'), TypeError),
            (tuple[int, str], (4, 2), TypeError),
            (tuple[float, str, bool], (3.14, 'b', True, 5), TypeError),
            (tuple[float, str | int, bool], (3.14, 2.6, True), TypeError),
            (set[bool], {True, 2}, TypeError),
            (set[int | str], {'a', 5, 3.14}, TypeError),
            (dict[str, int], {'a': 1, 'b': 'c'}, TypeError),
            (dict[str, float], {'a': 1.0, 2: 2.0}, TypeError),
            # Mixed types tests
            (list[dict[str, int]], [{'a': 1}, {'b': 2, 'c': 3}], None),
            (
                list[dict[str, dict[int, str]]],
                [{'a': {2: 'b'}}, {'b': {4: 'd'}, 'c': {5: 'e'}}],
                None,
            ),
            (
                dict[str, list[int | str]],
                {'a': [5, 'b', 6], 'b': ['c', 'd', 'e']},
                None,
            ),
            (
                dict[str, list[int | str]],
                {'a': [5, 'b', 6], 'b': ['c', 'd', 'e', 3.14]},
                TypeError,
            ),
            # Any types tests
            (Any, 'a', None),
            (Any, 2, None),
            (Any, 3.14, None),
            (Any, True, None),
            (Any, [1, 2], None),
            (Any, [1, 'a', True, 3.14], None),
            (Any, {'a': 1, 2: 'b'}, None),
            (list[Any], [1, 2], None),
            (list[Any], ['a', 'b'], None),
            (list[Any], ['a', 2, True, 3.14], None),
            (tuple[Any, str, Any], ('a', 'b', True), None),
            (dict[str, Any], {'a': 1, 'b': [1, 2]}, None),
            (dict[Any, Any], {'a': 1, 1: [1, 2]}, None),
            (
                dict[str, list[Any]],
                {'a': ['a', True, 3.14], 'b': [1, '2']},
                None,
            ),
            (Callable, lambda x: None, None),
            (Callable[[Any], Any], lambda x: None, None),
            (Callable[[int, str], int], lambda x: None, None),
            (Callable[[int, str], int], 'any', TypeError),
            (list[Any], {'a': 1}, TypeError),
            (tuple[Any, str, Any], ('a', 1, True), TypeError),
            (dict[str, Any], {'a': 1, 1: [1, 2]}, TypeError),
            (dict[str, list[Any]], {'a': 1, 'b': [1, 2]}, TypeError),
            # Custom types tests (check if not analyzed)
            (T, 'hello', None),
            (list[T], [1, 'a', 3.14], None),
            (list[T], {1, 'a', 3.14}, TypeError),
        ],
    )
    def test_inspect(
        self,
        type_: Any,
        value: Any,
        throwable: TypeError | None,
    ) -> None:
        inspector: Introspector = Introspector(type_, value)

        if throwable:
            with pytest.raises(throwable):
                inspector.inspect()
        else:
            inspector.inspect()

    @pytest.mark.parametrize(
        'type_, expected',
        [
            (int, int),
            (float, float),
            (str, str),
            (bool, bool),
            (list[str], list),
            (dict[str, Any], dict),
            (set[int], set),
            (tuple[int, int], tuple),
            (Any, Any),
        ],
    )
    def test__get_origin(self, type_: TypeVar, expected: TypeVar) -> None:
        inspector: Introspector = Introspector(type_, None)
        assert inspector._get_origin(type_) == expected

    @pytest.mark.parametrize(
        'type_, value, throwable',
        [
            (int, 200, None),
            (float, 3.14, None),
            (str, 'foo', None),
            (int | float, 'a', TypeError),
            (int | float, True, TypeError),
            (list[int], [1, 2, 3, 4], None),
            (tuple[str, str], (2, 'b'), None),
            (list[Any], ['a', 2, True, 3.14], None),
            (tuple[Any, str, Any], ('a', 1, True), None),
            (dict[str, Any], {'a': 1, 1: [1, 2]}, None),
            (list[int], (1, 2, 3, 4), TypeError),
            (list[Any], {'a', 2, True, 3.14}, TypeError),
            (list[Any], {'a': 1}, TypeError),
            (dict[str, Any], ('a', 1, 2), TypeError),
        ],
    )
    def test__inspect_origin(
        self,
        type_: TypeVar,
        value: Any,
        throwable: TypeError | None,
    ) -> None:
        inspector: Introspector = Introspector(type_, value)

        if throwable:
            with pytest.raises(throwable):
                inspector._inspect_origin(type_, value)
        else:
            inspector._inspect_origin(type_, value)

    @pytest.mark.parametrize(
        'type_, value, throwable',
        [
            (list[int], [1, 2, 3, 4], None),
            (tuple[str, str], ('a', 'b'), None),
            (list[Any], ['a', 2, True, 3.14], None),
            (tuple[Any, str, Any], ('a', 'b', True), None),
            (set[int], {1, 2}, None),
            (set[float], {1.2, 3.14}, None),
            (dict[str, Any], {'a': 1, 'b': [1, 2]}, None),
            (list[int], [1, 2, 'a', 4], TypeError),
            (dict[str, Any], {'a': 'b', 1: []}, TypeError),
        ],
    )
    def test__inspect_subtypes(
        self,
        type_: TypeVar,
        value: Any,
        throwable: TypeError | None,
    ) -> None:
        inspector: Introspector = Introspector(type_, value)

        if throwable:
            with pytest.raises(throwable):
                inspector._inspect_subtypes(type_, value)
        else:
            inspector._inspect_subtypes(type_, value)
