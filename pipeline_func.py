"""
A utility for calling functions in pipelines.
"""

__version__ = '0.0.0'

class PipelineFunc:

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __ror__(self, other):
        return self.func(other, *self.args, **self.kwargs)

f = PipelineFunc

