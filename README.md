# 🔍 v6e

[![PyPI version](https://badge.fury.io/py/v6e.svg)](https://badge.fury.io/py/v6e)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/license/mit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/v6e.svg)](https://pypi.org/project/v6e/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/v6e)](https://pypi.org/project/v6e/)
[![Contributors](https://img.shields.io/github/contributors/danimelchor/v6e)](https://github.com/danimelchor/v6e/graphs/contributors)

A simple, type-safe, and extensible Python parsing and validation framework

### Why the name?

`v6e` comes from the [numeronym](https://en.m.wikipedia.org/wiki/Numeronym) of "validate".

## Usage

```python
import v6e as v

my_parser = v.int().gte(18).lte(21)

# Use it only to check if the value conforms
my_parser.check(18)  # True
my_parser.check(21)  # True
my_parser.check(54)  # False

# Use `.parse()` (or call it) to validate and get the parsed value
my_parser.parse(21)  # Ok -> Returns 21 (int)
my_parser.parse("21")  # Ok -> Returns 21 (int)
my_parser.parse(54)  # Err -> Raises a ParseException
my_parser(54)  # Err -> Raises a ParseException
```

`v6e` also supports [custom parsers](https://github.com/danimelchor/v6e/tree/master/docs/index.md#custom-parsers), [custom reusable types](https://github.com/danimelchor/v6e/tree/master/docs/index.md#custom-reusable-types), [unions of parsers](https://github.com/danimelchor/v6e/tree/master/docs/index.md#custom-reusable-types), and more. See more in our [docs](https://github.com/danimelchor/v6e/tree/master/docs/index.md)!

## Examples

Check out the examples in `./examples`! You can run them locally with:

```
uv run examples/parsers.py
```

## 🐍 Type-checking

This library is fully type-checked. This means that all types will be correctly inferred
from the arguments you pass in.

In this example your editor will correctly infer the type:
```python
my_parser = v.int().gte(8).lte(4)
t.reveal_type(my_parser)  # Type of "my_parser" is "V6eInt"
t.reveal_type(my_parser.check)  # Type of "my_parser.check" is "(raw: Any) -> bool"
t.reveal_type(my_parser.safe_parse)  # Type of "my_parser" is "(raw: Any) -> V6eResult[int]"
t.reveal_type(my_parser.parse)  # Type of "my_parser" is "(raw: Any) -> int"
t.reveal_type(my_parser.__call__)  # Type of "my_parser" is "(raw: Any) -> int"
```

## Why should I care?

Type checking will help you catch issues way earlier in the development cycle. It will also
provide nice autocomplete features in your editor that will make you faster ⚡.

---

### Alpha notice

This project is still in its `alpha` phase. Expect frequent and breaking changes. You can see
more in our [planned work doc](https://github.com/danimelchor/v6e/blob/master/PLANNED_WORK.md).
