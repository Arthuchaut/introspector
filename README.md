# Introspector

[WIP] A Python library to write strongly typed code.

## Table of contents
- [Introspector](#introspector)
  - [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Basic usage](#basic-usage)

## Introduction

Introduce strict typing in your functions.  
This project is under development. 

## Basic usage

```py
import introspector

@introspector.strict
def foo(a: int, b: list[dict[str, Any]]) -> list[int]:
    # Some funny code...

    return [1, 2, 3, 4]

foo(
    42, 
    [
        {
            'x': ['hello', 'world'],
            'y': 3.14,
        },
    ],
)
```

When the code is executed, the `instrospector.strict` decorator will inspect the signature of the `foo` function and compare it with the values passed in its parameters.  
If the typing of the values does not match the signature of the function, introspector will throw a `TypeError` exception.