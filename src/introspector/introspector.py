from types import UnionType
from typing import Any, TypeVar, Union
from collections import abc


class Introspector:
    '''The inspector class implementation.
    Offer tool to compare a typing to a value.
    '''

    def __init__(self, type_tree: TypeVar) -> None:
        self._type_tree: TypeVar = type_tree

    def inspect(self, type_: TypeVar, value: Any) -> None:
        '''Analyze the typing tree and compare each typing node
        with the given value.

        Args:
            type_ (TypeVar): The typing tree.
            value (Any): The value to analyze.

        Raises:
            TypeError: If the value data structure does not match
                with the given typing.
        '''

        origin: TypeVar = self._get_origin(type_)

        if origin != Any and value is not None and type(origin) is not TypeVar:
            self._inspect_origin(type_, value)

            if hasattr(type_, '__args__') and type_.__args__:
                self._inspect_subtypes(type_, value)

    def _get_origin(self, type_: TypeVar) -> TypeVar:
        '''Get the original typing class.

        Args:
            type_ (TypeVar): The typing var.

        Returns:
            TypeVar: The original typing class.
        '''

        if hasattr(type_, '__origin__'):
            return type_.__origin__

        return type_

    def _inspect_origin(self, type_: TypeVar, value: Any) -> None:
        '''Analyze the main type.
        Example:
            - list[int]: main type is list
            - dict[str, Any]: main type if dict

        Args:
            type_ (TypeVar): The type var.
            value (Any): The value to analyze.

        Raises:
            TypeError: If the value data structure does not match
                with the given typing.
        '''

        origin: TypeVar = self._get_origin(type_)

        if type(origin) is UnionType or origin == Union:
            match: bool = False
            args: list[TypeVar] = (
                origin.__args__
                if hasattr(origin, '__args__')
                else type_.__args__
            )

            for sub_type in args:
                try:
                    self.inspect(sub_type, value)
                    match = True
                    break
                except TypeError:
                    pass

            if not match:
                raise TypeError(
                    f'Expected {self._type_tree}. Mismatch on {type(value)}'
                )
        elif (
            origin is not abc.Callable
            and origin is not type(value)
            or origin is abc.Callable
            and not isinstance(value, abc.Callable)
        ):
            raise TypeError(
                f'Expected {self._type_tree}. Mismatch on {type(value)}'
            )

    def _inspect_subtypes(self, type_: TypeVar, value: Any) -> None:
        '''Analyze the subtypes of the main type.
        Example:
            - list[int]: subtype is int
            - dict[str, Any]: subtypes are (str, Any)

        Args:
            type_ (TypeVar): The type var.
            value (Any): The value to analyze.

        Raises:
            TypeError: If the value data structure does not match
                with the given typing.
        '''

        origin: TypeVar = self._get_origin(type_)

        if origin is list:
            for item in value:
                self.inspect(type_.__args__[0], item)
        elif origin is tuple:
            if len(type_.__args__) != len(value):
                raise TypeError('Tuple sizes doesn\'t matches.')

            for i, sub_type in enumerate(type_.__args__):
                self.inspect(sub_type, value[i])
        elif origin is set:
            for item in value:
                self.inspect(type_.__args__[0], item)
        elif origin is dict:
            if len(type_.__args__) != 2:
                raise TypeError('Missing key/val in dict type definition.')

            for key, val in value.items():
                self.inspect(type_.__args__[0], key)
                self.inspect(type_.__args__[1], val)
