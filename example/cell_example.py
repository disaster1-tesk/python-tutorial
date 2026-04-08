from typing import Callable


def enclose_function() -> Callable[[], None]:
    print("enclose function execute")
    age =10
    def local_func():
        print("local_func:", age)
    return local_func

f = enclose_function()

print(f.__closure__)
print(hex(id(f)))
print(f)

