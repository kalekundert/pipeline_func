Pipeline Functions
==================
[![Last release](https://img.shields.io/pypi/v/pipeline_func.svg)](https://pypi.python.org/pypi/pipeline_func)
[![Python version](https://img.shields.io/pypi/pyversions/pipeline_func.svg)](https://pypi.python.org/pypi/pipeline_func)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/pipeline_func/test.yml?branch=master)](https://github.com/kalekundert/pipeline_func/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/pipeline_func)](https://app.codecov.io/github/kalekundert/pipeline_func)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/pipeline_func?logo=github)](https://github.com/kalekundert/pipeline_func)

*Pipeline Functions* is a simple utility for calling functions in "pipelines", 
i.e. where the output from one function is automatically the input for the 
next.  Here's an example showing how this works:

```pycon
>>> from pipeline_func import f
>>> def keep_odd(items):
...     return [x for x in items if x % 2 == 1]
>>> def keep_greater(items, threshold):
...     return [x for x in items if x > threshold]
>>> range(10) | f(keep_odd) | f(keep_greater, 4)
[5, 7, 9]
```

Contrast this to the harder-to-read style required to call these same functions 
without this library:
```pycon
>>> numbers = range(10)
>>> numbers = keep_odd(numbers)
>>> keep_greater(numbers, 4)
[5, 7, 9]
```

The only API provided by this library is the `f` function.  The first argument 
should be a callable object.  The remaining arguments can be arbitrary 
positional or keyword arguments.  Call the function by using the `|` operator 
as shown above.  The output from the left-hand side of the operator will be the 
first argument to the function.  Any extra arguments provided to `f()` will be 
added after.

This library only works if each pipeline function has exactly one input and one 
output.  It also requires that the initial input object does not implement the 
left `|` operator for `pipeline_func.PipelineFunc` objects. This should be true 
for any well-behaved object, though.
