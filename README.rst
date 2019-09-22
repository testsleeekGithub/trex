
Another useful tool in porting to python3 is ``pylint``. It is a code
analyzer that can catch errors in the code without running it.
If you run ``pylint`` with ``--py3k`` flag it reports code incompatible
with Python3::

    pylint --py3k example.py


Unpacking arguments also could be used in lambda functions in python2:

>>> # Python2 example
>>>
>>> f = lambda a, (b, c): (a, b, c)
>>> f(1, (2, 3))
(1, 2, 3)

This does not work in python3:

>>> # Python3 example
>>>
>>> f = lambda a, (b, c): (a, b, c)
SyntaxError: invalid syntax

In Python 3, we can raise and catch only instance of :py:`BaseException`
class or its subclasses

>>> # Python3 example
>>>
>>> class A: pass
>>> class B(BaseException): pass
>>> raise A
TypeError: exceptions must derive from BaseException
>>> if True: raise B
if True: raise B
B


In Python 3, so called star imports in classes and functions are not allowed

.. code-block:: python

    # This is SyntaxError in python3
    def f():
        from math import *
        return sin(1.3)

    class A:
        from os import *
        pass


In Python2, reading from a file opened by `open()` yielded the generic `str`.
>>> # Python2 example
>>>
>>> f = open('setup.py', 'rb')
>>> type(f)
file
>>> type(f.read())
str
>>> f = open('setup.py', 'r')
>>> type(f)
file
>>> type(f.read())
str

In Python3, the type of file contents depends on the mode the file was opened with:

>>> # Python3 example
>>>
>>> f = open('setup.py', 'rb')
>>> type(f)
_io.BufferedReader
>>> type(f.read())
bytes
>>> f= open('setup.py', 'r')
>>> type(f)
_io.TextIOWrapper
>>> type(f.read())
str


In python 2 dictionaries have :py:`has_key()` method

>>> # Python2 example
>>>
>>> dictionary.has_key('keyname')
False


In python3 :py:`has_key()` method is removed
>>> # Python3 example
>>>
>>> dictionary.has_key('keyname')
AttributeError: 'dict' object has no attribute 'has_key'

But you can use :py:`in` to do the same thing:

>>> # Python3 and python2 example
>>>
>>> 'key' in dictionary
False



The methods :py:`dict.iterkeys()`, :py:`dict.iteritems()` :py:`dict.itervalues()`, :py:`dict.viewkeys()`, :py:`dict.viewitems()`
and :py:`dict.viewvalues()`, are not available in python3.
The methods :py:`dict.keys()`, :py:`dict.items()` and :py:`dict.values()`
instead of lists return set like objects:

.. code-block:: python

    # Python3 example

    for x in d.keys():
        pass
    if y in d.values():
        pass
    z = len(d.items())

    # set operations
    symmetric_difference = d.keys() ^ d2.keys()
    union = d.values() | d2.values()
    intersection = d.items() & d2.items()


Be careful, if the underlying dictionary is modified, all assigned :py:`keys`, :py:`values`, and :py:`items`
are also modified

>>> # Python3 example
>>> x = {'a': 1, 'b': 2, 'c': 3}
>>> k = d.keys()
>>> v = d.values()
>>> i = d.items()
>>> k
dict_keys(['a', 'b', 'c'])
>>> v
dict_values([1, 2, 3])
>>>> i
dict_items([('a', 1), ('b', 2), ('c', 3)])
>>> x['d'] = 4
>>> k
dict_keys(['a', 'b', 'c', 'd'])
>>> v
dict_values([1, 2, 3, 4])
>>> i
dict_items([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
>>>
>>> # Indexing also does not work with these objects
>>>
>>> k[1]
TypeError: 'dict_keys' object does not support indexing
>>> v[1]
TypeError: 'dict_values' object does not support indexing
>>> i[1]
TypeError: 'dict_items' object does not support indexing
