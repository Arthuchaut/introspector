from typing import Any, Callable, TypeVar
import inspect
from .introspector import Introspector


def strict(*, exclude: list[str] = []) -> Callable[[Any], Any]:
    '''The strict decorator envelop.

    Args:
        exclude (Optional, list[str]): The list of excluded args.
            Default to [].

    Returns:
        Callable[[Any], Any]: The decorator function.
    '''

    if type(exclude) is not list:
        raise TypeError('Arg \'exclude\' must be the type of list[str].')

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        '''Decorator implementation for the function inspection.

        Args:
            func (Callable[[Any], Any]): The function to inspect.

        Raises:
            TypeError: If the function params types does not match with the
                given values.

        Returns:
            Callable[[Any], Any]: The decorator wrapper.
        '''

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            '''The decotator wrapper implementation.

            Args:
                *args (Any): The func arguments.
                **kwargs (Any): The func named arguments.

            Raises:
                TypeError: If the func params types does not match with the
                    given values or if any argument is not typed.

            Returns:
                Any: The func return value.
            '''

            sign: inspect.Signature = inspect.signature(func)
            parameters: dict[str, Any] = dict(sign.parameters)
            params_mapping: dict[str, tuple[TypeVar, Any]] = {}

            # Mapping kwargs parameters
            for arg_name, arg_val in kwargs.items():
                params_mapping[arg_name] = (
                    parameters[arg_name].annotation,
                    arg_val,
                )
                del parameters[arg_name]

            # Mapping args parameters
            for arg_name, arg_val in zip(parameters, args):
                params_mapping[arg_name] = (
                    parameters[arg_name].annotation,
                    arg_val,
                )

            # Mapping default parameters
            for arg_name, param in parameters.items():
                if param.default != inspect._empty:
                    params_mapping[arg_name] = (
                        param.annotation,
                        param.default,
                    )

            # Inspect func
            for arg_name, pair in params_mapping.items():
                if arg_name not in exclude:
                    try:
                        type_, value = pair

                        if type_ is inspect._empty:
                            raise TypeError('Missing typing.')

                        inspector: Introspector = Introspector(type_)
                        inspector.inspect(type_, value)
                    except TypeError as e:
                        raise TypeError(
                            f'[{func.__name__}{sign}] Arg '
                            f'\'{arg_name}\' error. {e}'
                        )

            # Calling func and retrieving its return value
            retval: Any = func(*args, **kwargs)

            # Inspect the func return value
            try:
                inspector: Introspector = Introspector(sign.return_annotation)
                inspector.inspect(sign.return_annotation, retval)
            except TypeError as e:
                raise TypeError(
                    f'[{func.__name__}{sign}] Return value error. {e}'
                )

            return retval

        return wrapper

    return decorator
