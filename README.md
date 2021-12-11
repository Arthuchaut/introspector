# Introspector

[WIP] A Python library to write strongly typed code.

## Table of contents
- [Introspector](#introspector)
  - [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Intended use](#intended-use)

## Introduction

Introduce strict typing in your functions.  
This project is under development. 

## Intended use

```py
import introspector

class Vector(tuple):
    ...

@introspector.strict
def foo(a: float, b: list[dict[str, int]]) -> list[Vector]:
    ...

PI: float = 3.14
pixels: list[dict[str, int]] = [
    {
        'x': 254,
        'y': 1564,
    },
    {
        'x': 456,
        'y': 342,
    },
]

foo(PI, pixels)
```

When the code is executed, the `instrospector.strict` decorator will inspect the signature of the `foo` function and compare it with the values passed in its parameters.  
If the typing of the values does not match the signature of the function, introspector will throw a `TypeError` exception.