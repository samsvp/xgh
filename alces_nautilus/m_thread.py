# %%
from typing import Any, Callable
from threading import Thread

x = 1

def f() -> int:
    global x
    x += 1
    return x


def g() -> int:
    global x
    x *= 5
    return x


def m_print(function: Callable) -> Any:
    global x
    for _ in range(100):
        a = function()
        print(a)
    return a


Thread(target=m_print, args=[f]).start()
Thread(target=m_print, args=[g]).start()
# %%
