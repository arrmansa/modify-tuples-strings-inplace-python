class modify_tuple:
    from ctypes import c_long, c_size_t, py_object, pythonapi

    pythonapi.PyTuple_SetItem.argtypes = (py_object, c_size_t, py_object)

    def __new__(cls, tup: tuple, idx: int, newval) -> tuple:
        # TYPE ERRORS
        if type(tup) is not tuple:
            raise TypeError(f"{tup} is not a tuple")
        if idx not in range(len(tup)):
            raise IndexError(f"{idx} is a bad index for {tup}")
        # ACTUAL CODE
        cls.pythonapi.Py_IncRef(newval)
        tupobj = cls.py_object(tup)
        reference_pointer = cls.c_long.from_address(id(tup))
        original_refcount = reference_pointer.value
        reference_pointer.value = 1
        cls.pythonapi.PyTuple_SetItem(tupobj, idx, newval)
        reference_pointer.value = original_refcount
        return tup

class modify_string:
    from ctypes import memmove
    from sys import getsizeof

    offset = getsizeof("") - 1

    def __new__(cls, text: str, start: int, newtext: str) -> str:
        # TYPE ERRORS
        if type(text) is not str or type(newtext) is not str:
            raise TypeError("got non string arguments")
        if len(newtext) + start > len(text):
            raise IndexError("Can't go over the length of the string")
        # ACTUAL CODE
        cls.memmove(id(text) + cls.offset + start, id(newtext) + cls.offset, len(newtext))
        return text

class modify_float:
    from ctypes import memmove
    from struct import pack
    from sys import getsizeof

    offset = getsizeof(float(0)) - len(pack("@d", 0))

    def __new__(cls, old: float, new: float) -> float:
        if type(old) is not float or type(new) is not float:
            raise TypeError("got non float arguments")
        new_data = cls.pack("@d", new)
        cls.memmove(id(old) + cls.offset, new_data, len(new_data))
        return old

my_tuple = (1, 2, 3)
print(my_tuple, id(my_tuple))
modify_tuple(my_tuple, 1, "hello")
print(my_tuple, id(my_tuple), (1, 2, 3), (*range(1,4),))

my_string = "very cool python code"
print(my_string, id(my_tuple))
modify_string(my_string, 10, "ctype stuff")
print(my_string, id(my_tuple), "very cool python code", "a " + "very cool python code")

my_float = 1.1
modify_float(my_float, 0.1)
print(my_float, 1.1, my_float + 0.5, 1.1 + 0.5)
