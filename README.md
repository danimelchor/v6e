# 🔍 V6E

A simple, type-safe, and extensible Python validations framework

### Why the name?

`v6e` comes from the [numeronym](https://en.m.wikipedia.org/wiki/Numeronym) of "validate".

### Examples

Check out the examples in `./examples`! You can run them locally with:

```
uv run examples/validations.py
```

## Usage

**Basic validations**
```python
import v6e

my_validation = v6e.Range(18, 21)

# Using it like a function
my_validation(18)  # True
my_validation(21)  # True
my_validation(54)  # False

# .ensure(...)
my_validation.ensure(21)  # Nothing happens -> continue to next line
my_validation.ensure(54)  # Raises a ValidationException
```

**`AND` and `OR` validations**
```python
my_validation = (v6e.StartsWith("foo") | v6e.EndsWith("foo")) & v6e.ReMatch(r"^[a-z0-9]*$")
my_validation("foo12")  # True
my_validation("12foo")  # True
my_validation("1foo2")  # False
```

**Custom validations**
```python
def is_div_three(x: int):
    if x % 3 != 0:
        raise ValueError("Woops! The Earth is 4.543 billion years old. (Try 4543000000)")

my_validation = v6e.Custom(is_div_three)
my_validation(3)  # True
my_validation(6)  # True
my_validation(4)  # False
```

## 🐍 Type-checking

This library is fully type-checked. This means that all types will be correctly inferred
from the arguments you pass in.

In this example your editor will correctly infer the type:
```python
my_validation = v6e.Choices([2,3]) | v6e.Range(1, 4)
reveal_type(my_validation)  # Type of "res" is "_Union[int]" (compatible with "Callable[[int], None]")
```

## Why do I care?

Type checking will help you catch issues way earlier in the development cycle. It will also
provide nice autocomplete features in your editor that will make you faster ⚡.
