from pipeline_func import f

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
