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
import v6e as v

my_validation = v.int().gte(18).lte(21)

# Use it only to check if the value conforms
my_validation.check(18)  # True
my_validation.check(21)  # True
my_validation.check(54)  # False

# Use `.parse()` to validate and get the parsed value
my_validation.parse(21)  # Ok -> Returns 21 (int)
my_validation.parse("21")  # Ok -> Returns 21 (int)
my_validation.parse(54)  # Err -> Raises a ValidationException
```

**Chaing your validations and transformations**
```python
my_validation = v.str().trim().starts_with("foo").ends_with("foo").regex(r"^[a-z0-9]*$")
my_validation.parse("  foo12")  # Ok -> Returns 'foo12' (str)
my_validation.parse("12foo  ")  # Ok -> Returns '12foo' (str)
my_validation.parse("1foo2")  # Err -> Raises a ValidationException
```

**Custom validations**
```python
class DivThree(v.IntType):
    @override
    def _parse(self, raw: t.Any):
        parsed: int = super()._parse(raw)
        if parsed % 3 != 0:
            raise ValueError(f"Woops! {parsed!r} is not divisible by three")


my_validation = DivThree().gt(5)
my_validation(6)  # Ok -> Returns 6
my_validation(3)  # Err (not >5) -> Raises a ValidationException
my_validation(7)  # Err (not div by 3) -> Raises a ValidationException
```

## 🐍 Type-checking

This library is fully type-checked. This means that all types will be correctly inferred
from the arguments you pass in.

In this example your editor will correctly infer the type:
```python
my_validation = v.int().gte(8).lte(4)
t.reveal_type(my_validation)  # Type of "my_validation" is "V6eInt"
t.reveal_type(my_validation.check)  # Type of "my_validation.check" is "(raw: Any) -> bool"
t.reveal_type(my_validation.safe_parse)  # Type of "my_validation" is "(raw: Any) -> ParseResult[int]"
t.reveal_type(my_validation.parse)  # Type of "my_validation" is "(raw: Any) -> int"
```

## Why do I care?

Type checking will help you catch issues way earlier in the development cycle. It will also
provide nice autocomplete features in your editor that will make you faster ⚡.
