from typing import Any, Callable, ClassVar, TypeVar
import inspect
from .introspector import Introspector


class Strict:
    '''The Strict class decorator.
    This is the entry point to control the function parameters.

    Examples:
        @Strict
        def foo(a: int, b: list[str]) -> None:
            ...

        @Strict(exclude=['b'])
        def bar(a: int, b: list[str]) -> None:
            ...

    Attributes:
        _fx (Callable[[Any], Any]): The function reference.
        _fx_sign (inspect.Signature): The function signature.
        _exclude (set[str]) = The list of arguments that will not
            inspected. Default to _DEFAULT_EXCLUSIONS.
        _DEFAULT_EXCLUSIONS (ClassVar[list[str]]) The default list of
            excluded function arguments.
    '''

    _DEFAULT_EXCLUSIONS: ClassVar[list[str]] = ['self', 'cls']

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        '''The constructor.

        Args:
            *args (Any): Optional arguments.
            **kwargs (Any): Optional named arguments.
        '''

        self._fx: Callable[[Any], Any] = None
        self._fx_sign: inspect.Signature = None
        self._exclude: set[str] = set(kwargs.get('exclude', []))
        self._exclude.update(self._DEFAULT_EXCLUSIONS)

    def _map_params(
        self,
        *fx_args: Any,
        **fx_kwargs: Any,
    ) -> dict[str, tuple[TypeVar, Any]]:
        '''Build a mapping of the function given arguments and the
        function signature.

        Examples:
            This method should returns a data like:
                {
                    'a': (int, 42),
                    'b': (list[str], [5, 'string']),
                }

        Args:
            *fx_args (Any): The function arguments.
            **fx_kwargs (Any): The function named arguments.

        Returns:
            dict[str, tuple[TypeVar, Any]]: The parameters mapping.
        '''

        params: dict[str, Any] = dict(self._fx_sign.parameters)
        params_mapping: dict[str, tuple[TypeVar, Any]] = {}

        # Mapping kwargs parameters
        for arg_name, arg_val in fx_kwargs.items():
            params_mapping[arg_name] = (
                params[arg_name].annotation,
                arg_val,
            )
            del params[arg_name]

        # Mapping args parameters
        for arg_name, arg_val in zip(params, fx_args):
            params_mapping[arg_name] = (
                params[arg_name].annotation,
                arg_val,
            )

        # Mapping default parameters
        for arg_name, param in params.items():
            if param.default != inspect._empty:
                params_mapping[arg_name] = (
                    param.annotation,
                    param.default,
                )

        return params_mapping

    def _inspect_fx_sign(self, *fx_args: Any, **fx_kwargs: Any) -> None:
        '''Control the function given parameters.

        Args:
            *fx_args (Any): The function arguments.
            **fx_kwargs (Any): The function named arguments.

        Raises:
            TypeError: If any inspection detect a typing mismatch.
        '''

        params_mapping: dict[str, tuple[TypeVar, Any]] = self._map_params(
            *fx_args,
            **fx_kwargs,
        )

        for arg_name, pair in params_mapping.items():
            if arg_name not in self._exclude:
                try:
                    type_, value = pair

                    if type_ is inspect._empty:
                        raise TypeError('Missing typing.')

                    inspector: Introspector = Introspector(type_)
                    inspector.inspect(type_, value)
                except TypeError as e:
                    raise TypeError(
                        f'[{self._fx.__name__}] Arg '
                        f'\'{arg_name}\' error. {e}'
                    )

    def _inspect_fx_retval(self, retval: Any) -> None:
        '''Control the function return value.

        Args:
            retval (Any): The function return value.

        Raises:
            TypeError: If the function return value does not match the
                signature.
        '''

        try:
            inspector: Introspector = Introspector(
                self._fx_sign.return_annotation
            )
            inspector.inspect(self._fx_sign.return_annotation, retval)
        except TypeError as e:
            raise TypeError(f'[{self._fx.__name__}] Return value error. {e}')

    def __call__(self, fx: Callable[[Any], Any]) -> Any:
        '''The __call__ implementation.
        When using this class with the decorator syntax, this method is call.

        Args:
            fx (Callable[[Any], Any]): The function reference.

        Raises:
            TypeError: If any function values does not match with the function
                signature.
            ValueError: If the given fx argument is not a Callable.

        Returns:
            Any: The function return value.
        '''

        def wrapper(*fx_args: Any, **fx_kwargs: Any) -> Any:
            '''The decorator inner function.
            Apply the function controls.

            Args:
                *fx_args (Any): The function arguments.
                **fx_kwargs (Any): The function named arguments.

            Raises:
                TypeError: If any function values does not match with the
                    function signature.

            Returns:
                Any: The function return value.
            '''

            self._inspect_fx_sign(*fx_args, **fx_kwargs)
            retval: Any = self._fx(*fx_args, **fx_kwargs)
            self._inspect_fx_retval(retval)
            return retval

        if not callable(fx):
            raise ValueError('Expected callable at 1st arg.')

        self._fx = fx
        self._fx_sign = inspect.signature(self._fx)
        return wrapper
