#%%
from typing import *

class pipe:
    def __init__(self, x: Any) -> None:
        self.x = x
    
    
    def __rshift__(self, f) -> "pipe":
        if hasattr(f, '__iter__'):
            self.x = f[0](*f[1:]) if len(f) > 2 else f[0](f[1], self.x)
        else:
            self.x = f(self.x)
        return self
    
    def __str__(self) -> str:
        return str(self.x)
    
#%%
if __name__ == "__main__":    
    (p := pipe(range(10))) >> (map, lambda x: 2*x) \
        >> (filter, lambda x: x % 3 ==0) \
        >> sum >> (lambda x: x / 2)
    
    print(p.x)

# %%
