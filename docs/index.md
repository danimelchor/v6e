## Types

### Integers

```python
v.int()  # or v.V6eInt()

v.int().gt(5)
v.int().gte(5)
v.int().lt(5)
v.int().lte(5)
v.int().min(5)
v.int().max(5)

v.int().positive()
v.int().nonpositive()
v.int().negative()
v.int().nonnegative()
v.int().multiple_of(5)
v.int().step(5)
```

### Floats

```python
v.float()  # or v.V6eFloat()

v.float().gt(5)
v.float().gte(5)
v.float().lt(5)
v.float().lte(5)
v.float().min(5)
v.float().max(5)

v.float().positive()
v.float().nonpositive()
v.float().negative()
v.float().nonnegative()
v.float().multiple_of(5)
v.float().step(5)
```

### Strings

```python
v.str()  # or v.V6eStr()

v.str().length(5)
v.str().contains("abc")

v.str().starts_with("abc")
v.str().ends_with("abc")
v.str().regex(r"^[a-c]$")
v.str().email()
v.str().uuid()

v.float().gt("a")
v.float().gte("a")
v.float().lt("a")
v.float().lte("a")
v.float().min("a")
v.float().max("a")
```

### Booleans

```python
v.bool()  # or v.V6eBool()

v.bool().is_true()
v.bool().is_false()
```

### DateTimes

```python
v.datetime()  # or v.V6eDateTime

v.tz(timezone.utc)
```

### TimeDeltas

```python
v.timedelta()  # or v.V6eTimeDelta
```

### Dict

The `Dict` type is used to ensure the schema of a Python native `dict`. They're
composed of keys and the validation for that key. Extra keys are removed from the `dict`.

```python
v.dict(  # or v.V6eDict
    name=v.str(),
    age=v.int(),
)
```

### Struct

Similar to the `Dict` type, the `Struct` type is used to validate the fields inside an
object conform to the provided schema. Extra keys are left as they are.

```python
v.struct(  # or v.V6eStruct
    name=v.str(),
    age=v.int().lt(23),
)
```

## Chaining parsers

```python
my_parser = v.str().trim().starts_with("foo").ends_with("foo").regex(r"^[a-z0-9]*$")
my_parser.parse("  foo12")  # Ok -> Returns 'foo12' (str)
my_parser.parse("12foo  ")  # Ok -> Returns '12foo' (str)
my_parser.parse("1foo2")  # Err -> Raises a ParseException
```

## Union of parsers

```python
union = v.str().starts_with("foo") | v.int().gte(5)

union.parse("foobar")  # Ok -> Returns 'foobar' (str)
union.parse("1foo2")  # Err -> Raises a ParseException

union.parse(5)  # Ok -> Returns 5 (int)
union.parse(3)  # Err -> Raises a ParseException

union.parse(None)  # Err -> Raises a ParseException
```

## Custom parsers

```python
def _validate_earth_age(x: int) -> None:
    if x != 4_543_000_000:
        raise ValueError("The Earth is 4.543 billion years old. Try 4543000000.")

earth_age = v.int().custom(_validate_earth_age)
earth_age.parse(4_543_000_000)  # Ok -> Returns 4_543_000_000 (int)
earth_age.parse("4543000000")  # Ok -> Returns 4_543_000_000 (int)
earth_age.parse(1)  # Err -> Raises ParseException
```

## Custom reusable types

```python
class DivThree(v.IntType):
    @override
    def parse_raw(self, raw: t.Any):
        parsed: int = super().parse_raw(raw)
        if parsed % 3 != 0:
            raise ValueError(f"Woops! {parsed!r} is not divisible by three")


my_parser = DivThree().gt(5)
my_parser.parse(6)  # Ok -> Returns 6
my_parser.parse(3)  # Err (not >5) -> Raises a ParseException
my_parser.parse(7)  # Err (not div by 3) -> Raises a ParseException
```
