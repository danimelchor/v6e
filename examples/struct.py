import argparse
from dataclasses import dataclass

import v6e as v
from examples.utils import print_example, print_title

# Define the parser
my_struct = v.struct(
    name=v.str(),
    age=v.int().lt(23),
)


@dataclass
class Args:
    name: str
    age: int


def dataclass_example():
    print_title("Dataclass example")

    obj = Args("daniel", 22)
    print_example(my_struct, obj)

    obj = Args("daniel", 24)
    print_example(my_struct, obj)


def argparse_example():
    print_title("Argparse example (pass in --name and --age)")
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--name")
    args_parser.add_argument("--age")
    args = args_parser.parse_args()
    print_example(my_struct, args)


if __name__ == "__main__":
    dataclass_example()
    argparse_example()
