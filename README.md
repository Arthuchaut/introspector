# Introspector

[WIP] A Python library to write strongly typed code.

## Table of contents
- [Introspector](#introspector)
  - [Table of contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [From Pypi](#from-pypi)
    - [From releases](#from-releases)
  - [Basic usage](#basic-usage)
  - [Python 3.10 supported typing syntax](#python-310-supported-typing-syntax)
  - [Instrospector.strict available options](#instrospectorstrict-available-options)
    - [:arrow_right: ignore](#arrow_right-ignore)

## Introduction

Introduce strict typing in your functions.  
This project is under development. 

## Requirements

- Python >= 3.10

## Installation

### From Pypi

```sh
pip install introspector
```

### From releases

Go to the [releases](https://github.com/Arthuchaut/introspector/releases) page and download the `wheel` of the latest version.  
Then, add the whell file in your project folder and install it via pip.

```sh
pip install <path/to/introspector-*.whl>
```

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

## Python 3.10 supported typing syntax

This paclage support the following typing syntaxes:

| Name          | Description                    | Example        |
| ------------- | ------------------------------ | -------------- |
| `\|` operator | The Union type shortcut syntax | `int \| float` |

## Instrospector.strict available options

### :arrow_right: ignore

A list of parameter names that will be excluded from the typing control.  
Notice that the `ignore` option will always contains `self` and `cls`.

**Example:**

```py
@instrospector.strict(ignore=['b'])
def foo(a: int, b: float) -> None:
    ...
```

The argument `b` will be ignored by the typing control.
