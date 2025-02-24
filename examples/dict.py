import v6e as v
from examples.utils import print_example, print_title

# Define the parser
my_dict = v.dict(
    name=v.str(),
    age=v.int(),
)


def basic_example():
    print_title("Dict with name and age")
    obj = {"name": "daniel", "age": 22}
    print_example(my_dict, obj)

    obj2 = {"name": 16, "age": 22}
    print_example(my_dict, obj2)


def extra_keys_example():
    print_title("Dict with extra keys")
    obj = {"name": "daniel", "age": 22, "extra": 20}
    print_example(my_dict, obj)


if __name__ == "__main__":
    basic_example()
    extra_keys_example()
