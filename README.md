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

# .test(...)
my_validation.test(18)  # True
my_validation.test(21)  # True
my_validation.test(54)  # False

# .validate(...)
my_validation.validate(21)  # Nothing happens -> continue to next line
my_validation.validate(54)  # Raises a ValidationException()
```

**`AND` and `OR` validations**
```python
my_validation = (v6e.StartsWith("foo") | v6e.EndsWith("foo")) & v6e.ReMatch(r"^[a-z]*$")
my_validation.test("foo12")  # True
my_validation.test("12foo")  # True
my_validation.test("1foo2")  # False
```

**Custom validations**
```python
def is_div_three(x: int):
    if x % 3 != 0:
        raise ValueError("Woops! The Earth is 4.543 billion years old. (Try 4543000000)")

my_validation = v6e.Custom(validate_earth_age)
my_validation.test(3)  # True
my_validation.test(6)  # True
my_validation.test(4)  # False
```

## 🐍 Type-checking

This library is fully type-checked. This means that all types will be correctly inferred
from the arguments you pass in.

In this example your editor will correctly infer the type:
```python
my_validation = v6e.StartsWith("foo") | v6e.Range(1, 4)
reveal_type(hours)  # Type of "res" is "timedelta | str | int"
```

## Why do I care?

Type checking will help you catch issues way earlier in the development cycle. It will also
provide nice autocomplete features in your editor that will make you faster ⚡.
