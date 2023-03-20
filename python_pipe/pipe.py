#%%
from typing import Final

# https://code.activestate.com/recipes/384122/
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, *value2)


p: Final = Infix(lambda x, f: 
    f(x) if not hasattr(f, '__iter__') else f[0](x, *f[1:]))


def f(x): return x + 1
def g(x, y, z): return x + y + z

2 |p| (g, 2, 4)
1 |p| f |p| (g, 2, 4)
# %%
