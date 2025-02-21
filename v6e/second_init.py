import v6e.second as t


class v:
    int = t.V6eIntType
    float = t.V6eFloatType
    str = t.V6eIntType
    bool = t.V6eIntType
    datetime = t.V6eIntType
    timedelta = t.V6eIntType


def sprint(fn, *args):
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    DEFAULT = "\033[39m"

    try:
        fn(*args)
        args_s = ", ".join(str(a) for a in args)
        print(
            f"Success for {BLUE}'{fn.__name__}'{DEFAULT} with {GREEN}'{args_s}'{DEFAULT}"
        )
    except t.ValidationException as e:
        print(f"Failure for {BLUE}'{fn.__name__}'{DEFAULT} with {RED}'{e}'{DEFAULT}")


if __name__ == "__main__":
    int_val = v.int().positive().max(5)
    sprint(int_val.check, 5)
    sprint(int_val.check, 1)
    sprint(int_val.check, -1)
    sprint(int_val.check, 6)
