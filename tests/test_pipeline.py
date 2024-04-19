from pipeline_func import f, X
import pytest

def test_pipeline():

    def g(a):
        return a, 2

    def h(a):
        return a, 3

    assert 1 | f(g) == (1, 2)
    assert 1 | f(g) | f(h) == ((1, 2), 3)

def test_pipeline_args():

    def g(a, b):
        return a, b

    assert 1 | f(g, 2) == (1, 2)
    assert 1 | f(g, 2) | f(g, 3) == ((1, 2), 3)

def test_pipeline_kwargs():

    def g(a, *, b):
        return a, b

    assert 1 | f(g, b=2) == (1, 2)
    assert 1 | f(g, b=2) | f(g, b=3) == ((1, 2), 3)

def test_pipeline_kwargs_func():

    # Specifically test a function that takes a keyword argument named `func`. 
    # This is the same name as the first argument to `__init__()`, so care must 
    # be taken that the two names don't conflict.

    def g(a, *, func):
        return func(a)

    assert 1 | f(g, func=lambda x: (x, 2)) == (1, 2)

def test_pipeline_dataframe():
    import polars as pl

    # I plan to use this library with data frames, so I want to test it in that 
    # context.  Note that the code should work with any input type that doesn't 
    # implement the | operator for `PipelineFunc` objects.  This should include 
    # almost all well-behaved types.

    df = pl.DataFrame({'a': [1, 2, 3]})

    def g(df):
        return df.with_columns(b=pl.col('a') * 2)

    out = df | f(g)

    assert out.to_dicts() == [
            dict(a=1, b=2),
            dict(a=2, b=4),
            dict(a=3, b=6),
    ]
def test_placeholder_args():

    def g(a, b):
        return a, b

    assert 1 | f(g, X, 2) == (1, 2)
    assert 1 | f(g, 2, X) == (2, 1)
    assert 1 | f(g, X, X) == (1, 1)

def test_placeholder_kwargs():

    def g(*, a, b):
        return a, b

    assert 1 | f(g, a=X, b=2) == (1, 2)
    assert 1 | f(g, a=2, b=X) == (2, 1)
    assert 1 | f(g, a=X, b=X) == (1, 1)

def test_placeholder_getattr():

    class Pair:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    def g(a, b):
        return (a, b)

    assert Pair(1, 2) | f(g, X.a, 3) == (1, 3)
    assert Pair(1, 2) | f(g, X.b, 3) == (2, 3)

    with pytest.raises(AttributeError):
        Pair(1, 2) | f(g, X.c, 3)

    assert Pair(Pair(1, 2), Pair(3, 4)) | f(g, X.a.a, 5) == (1, 5)
    assert Pair(Pair(1, 2), Pair(3, 4)) | f(g, X.a.b, 5) == (2, 5)
    assert Pair(Pair(1, 2), Pair(3, 4)) | f(g, X.b.a, 5) == (3, 5)
    assert Pair(Pair(1, 2), Pair(3, 4)) | f(g, X.b.b, 5) == (4, 5)

    with pytest.raises(AttributeError):
        Pair(Pair(1, 2), Pair(3, 4)) | f(g, X.a.c, 5)

def test_placeholder_getitem():

    def g(a, b):
        return (a, b)

    assert [1, 2] | f(g, X[0], 3) == (1, 3)
    assert [1, 2] | f(g, X[1], 3) == (2, 3)
    assert [1, 2] | f(g, X[-1], 3) == (2, 3)
    assert [1, 2] | f(g, X[-2], 3) == (1, 3)

    with pytest.raises(IndexError):
        [1, 2] | f(g, X[3], 3)
    with pytest.raises(KeyError):
        {'a': 1, 'b': 2} | f(g, X['c'], 3)

    assert [[1, 2], [3, 4]] | f(g, X[0][0], 5) == (1, 5)
    assert [[1, 2], [3, 4]] | f(g, X[0][1], 5) == (2, 5)
    assert [[1, 2], [3, 4]] | f(g, X[1][0], 5) == (3, 5)
    assert [[1, 2], [3, 4]] | f(g, X[1][1], 5) == (4, 5)

    with pytest.raises(IndexError):
        [[1, 2], [3, 4]] | f(g, X[0][3], 3)
    with pytest.raises(KeyError):
        {'a': {'x': 1}, 'b': {'y': 2}} | f(g, X['a']['z'], 3)

def test_placeholder_getattr_getitem():

    class Pair:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    def g(a, b):
        return (a, b)

    assert Pair([1, 2], [3, 4]) | f(g, X.a[0], 5) == (1, 5)
    assert Pair([1, 2], [3, 4]) | f(g, X.a[1], 5) == (2, 5)
    assert Pair([1, 2], [3, 4]) | f(g, X.b[0], 5) == (3, 5)
    assert Pair([1, 2], [3, 4]) | f(g, X.b[1], 5) == (4, 5)

    assert [Pair(1, 2), Pair(3, 4)] | f(g, X[0].a, 5) == (1, 5)
    assert [Pair(1, 2), Pair(3, 4)] | f(g, X[0].b, 5) == (2, 5)
    assert [Pair(1, 2), Pair(3, 4)] | f(g, X[1].a, 5) == (3, 5)
    assert [Pair(1, 2), Pair(3, 4)] | f(g, X[1].b, 5) == (4, 5)

def test_placeholder_getattr_call():

    class Obj:
        def __init__(self, a):
            self.a = a

        def h(self, *args, **kwargs):
            return (self.a, *args, *kwargs.items())

    def g(a, b):
        return (a, b)

    assert Obj(1) | f(g, X.h(2), 3) == ((1, 2), 3)
    assert Obj(1) | f(g, X.h(2, 3), 4) == ((1, 2, 3), 4)
    assert Obj(1) | f(g, X.h(a=2), 4) == ((1, ('a', 2)), 4)
    assert Obj(1) | f(g, X.h(a=2, b=3), 4) == ((1, ('a', 2), ('b', 3)), 4)

def test_f_repr():

    def g(*args, **kwargs):
        pass

    assert repr(f(g)) == 'f(g)'
    assert repr(f(g, 1)) == 'f(g, 1)'
    assert repr(f(g, 'x')) == "f(g, 'x')"
    assert repr(f(g, X)) == "f(g, X)"
    assert repr(f(g, a=1)) == 'f(g, a=1)'
    assert repr(f(g, a='x')) == "f(g, a='x')"
    assert repr(f(g, a=X)) == "f(g, a=X)"
    assert repr(f(g, 1, a=2)) == 'f(g, 1, a=2)'
    assert repr(f(g, 'x', a='y')) == "f(g, 'x', a='y')"
    assert repr(f(g, X, a=X)) == "f(g, X, a=X)"

def test_X_repr():
    assert repr(X) == 'X'
    assert repr(X.a) == 'X.a'
    assert repr(X.a.b) == 'X.a.b'
    assert repr(X[1]) == 'X[1]'
    assert repr(X[1][2]) == 'X[1][2]'
    assert repr(X.a[1].b[2]) == 'X.a[1].b[2]'
    assert repr(X[1].a[2].b) == 'X[1].a[2].b'

    assert repr(X()) == 'X()'
    assert repr(X(1)) == 'X(1)'
    assert repr(X(a=1)) == 'X(a=1)'
    assert repr(X(1, a=2)) == 'X(1, a=2)'
    assert repr(X.a()) == 'X.a()'
    assert repr(X.a(1)) == 'X.a(1)'
    assert repr(X.a(b=1)) == 'X.a(b=1)'
    assert repr(X.a(1, b=2)) == 'X.a(1, b=2)'
