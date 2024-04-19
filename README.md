Pipeline Functions
==================
[![Last release](https://img.shields.io/pypi/v/pipeline_func.svg)](https://pypi.python.org/pypi/pipeline_func)
[![Python version](https://img.shields.io/pypi/pyversions/pipeline_func.svg)](https://pypi.python.org/pypi/pipeline_func)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/pipeline_func/test.yml?branch=master)](https://github.com/kalekundert/pipeline_func/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/pipeline_func)](https://app.codecov.io/github/kalekundert/pipeline_func)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/pipeline_func?logo=github)](https://github.com/kalekundert/pipeline_func)

*Pipeline Functions* is a simple utility for calling functions in "pipelines", 
i.e. where the output from one function is automatically the input for the 
next. Here's an example showing how this works:

```pycon
>>> from pipeline_func import f, X
>>> a = [3, 4, 2, 1, 0]
>>> b = [2, 1, 4, 0, 3]
>>> a | f(zip, b) | f(map, min, X) | f(filter, bool, X) | f(sorted)
[1, 2, 2]
```

To briefly explain, we start with two random lists of integers. We then find 
the smaller value in each position, discard any zeros, and sort whatever 
remains. Contrast the easily-readable pipeline syntax to what would be 
necessary without it:

```pycon
>>> sorted(filter(bool, map(min, zip(a, b))))
[1, 2, 2]
```

Installation
------------
*Pipeline Functions* is available on PyPI:
```
$ pip install pipeline_func
```
Version numbers obey [semantic versioning](https://semver.org/).

Documentation
-------------
This library provides a single function, named `f()`. The purpose of `f()` is 
to wrap another function such that it can be called as part of a pipeline. 
Below is the call signature for `f()`:

```
f(func: Callable[..., Any], /, *args: Any, **kwargs: Any)
```

The first argument to `f()` must be a function. The remaining arguments can be 
arbitrary positional and/or keyword arguments. `f()` produces a wrapped version 
of the given function which can subsequently be called using the `|` operator 
as shown above. By default, the value from the left-hand side of the operator 
will be the first argument to the function. Any extra arguments provided to `f` 
will be added after.

If it's not convenient for the incoming value to be the first argument to the 
wrapped function, you can use the `X` object to put the arguments in any order 
you want.  Think of `X` as a placeholder that will be replaced by the value 
from the previous step in the pipeline. `X` can be either a positional or a 
keyword argument, and can be used for multiple arguments at the same time.  You 
can also use attribute access syntax (e.g. `X.my_attr`), item lookup syntax 
(e.g. `X[key]`), function invocation syntax (e.g. `X(arg1, arg2)`), or any 
combination of the above (e.g. `X.my_method()[0]`) to easily extract 
information from the input value.

To make all of the above more concrete, here are some examples showing how 
`f()` can be used to call some common functions:

Pipeline | Equivalent to | Result
---|---|---
`[1, 2] \| f(min)` | `min([1, 2])` | `1`
`[1, 2] \| f(zip, [3, 4])` | `zip([1, 2], [3, 4])` | `[(1, 3), (2, 4)]`
`[1, 2] \| f(sorted, reverse=True)` | `sorted([1, 2], reverse=True)` | `[2, 1]`
`[1, 2] \| f(map, str, X)` | `map(str, [1, 2])` | `['1', '2']`

This library only works if each pipeline function has exactly one input and one 
output. It also requires that the initial input object does not implement the 
left `|` operator for `pipeline_func.PipelineFunc` objects. This should be true 
for any well-behaved object, though.
