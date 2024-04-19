"""
A utility for calling functions in pipelines.
"""

__version__ = '0.2.0'

from itertools import chain
from typing import Callable, Any

class PipelineFunc:

    def __init__(self, func: Callable[..., Any], /, *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

        has_placeholder = any(
                isinstance(x, PipelineArg)
                for x in chain(args, kwargs.values())
        )
        if has_placeholder:
            self._call = self._call_with_placeholder
        else:
            self._call = self._call_without_placeholder

    def __repr__(self) -> str:
        func_arg = [self.func.__name__]
        return _function_repr('f', func_arg, self.args, self.kwargs)

    def __ror__(self, other: Any) -> Any:
        return self._call(other)

    def _call_without_placeholder(self, other: Any) -> Any:
        return self.func(other, *self.args, **self.kwargs)

    def _call_with_placeholder(self, other: Any) -> Any:
        args = [
                x._PipelineArg__transform(other)
                if isinstance(x, PipelineArg) else x
                for x in self.args
        ]
        kwargs = {
                k: x._PipelineArg__transform(other)
                   if isinstance(x, PipelineArg) else x
                for k, x in self.kwargs.items()
        }
        return self.func(*args, **kwargs)

class PipelineArg:

    def __init__(
            self,
            transform: Callable[[Any], Any] = lambda x: x,
            repr: str = 'X',
    ):
        # Use private variables to minimize the number of names that 
        # `__getattr__()` can conflict with.
        self.__transform = transform
        self.__repr = repr

    def __repr__(self) -> str:
        return self.__repr

    def __getattr__(self, attr: str) -> 'PipelineArg':
        return PipelineArg(
                transform=lambda x: getattr(self.__transform(x), attr),
                repr=f'{self.__repr}.{attr}',
        )

    def __getitem__(self, key: str) -> 'PipelineArg':
        return PipelineArg(
                transform=lambda x: self.__transform(x)[key],
                repr=f'{self.__repr}[{key}]',
        )

    def __call__(self, *args: Any, **kwargs: Any) -> 'PipelineArg':
        return PipelineArg(
                transform=lambda x: self.__transform(x)(*args, **kwargs),
                repr=_function_repr(self.__repr, [], args, kwargs),
        )

def _function_repr(f, verbatim_args, args, kwargs):
    kwarg_reprs = [f'{k}={v!r}' for k, v in kwargs.items()]
    arg_reprs = map(repr, args)
    args_kwargs_repr = ", ".join(chain(verbatim_args, arg_reprs, kwarg_reprs))
    return f'{f}({args_kwargs_repr})'


f = PipelineFunc
X = PipelineArg()

