from __future__ import annotations

import re
import typing as t

from typing_extensions import override

import v6e as v
from examples.utils import print_example, print_title


# --- DEMO ---
def main() -> None:
    # Basic usage
    can_drink = v.int().gte(21)
    print_title("Basic - Age")
    print_example(can_drink, 21)
    print_example(can_drink, 20)

    # You can chain multiple checks
    interview_channel = v.str().startswith("#").regex("interview.*[0-9]{2}-[0-9]{2}")
    print_title("Chaining Parsers - Slack Channel")
    print_example(interview_channel, "#interview-foo-feb-01-12")
    print_example(interview_channel, "#foo-feb-01-12")

    # You can OR multiple parsers
    union = v.str().startswith("foo") | v.int().gte(5)
    print_title("Union of parsers - foo or 5")
    print_example(union, "foobar")
    print_example(union, "1foo2")
    print_example(union, 5)
    print_example(union, 4)
    print_example(union, None)

    # You can create your own custom parsers
    def _validate_earth_age(x: int) -> None:
        if x != 4_543_000_000:
            raise ValueError("The Earth is 4.543 billion years old. Try 4543000000.")

    earth_age = v.int().custom(_validate_earth_age)
    print_title("Custom Parser - Earth Age")
    print_example(earth_age, 4_543_000_000)
    print_example(earth_age, 4_543_000)

    # You can create your own reusable parser types or extend existing ones
    class SlackChannel(v.V6eStr):
        @override
        def parse_raw(self, raw: t.Any) -> str:
            parsed: str = super().parse_raw(raw)
            if re.search(r"^#[a-z0-9-]+$", parsed) is None:
                raise v.ParseException(
                    "Slack channels must start with '#' and contain only letters, numbers, and dashes"
                )

            return parsed

    foo_slack_channel = SlackChannel().contains("foo")
    print_title("Reusable Parser Type - Slack Channel")
    print_example(foo_slack_channel, "#foo-bar")
    print_example(foo_slack_channel, "foo-bar")

    # Type checking example
    print_title("Type-checking example")
    my_parser = v.int().gte(8).lte(4)
    print(my_parser)
    t.reveal_type(my_parser)
    t.reveal_type(my_parser.check)
    t.reveal_type(my_parser.safe_parse)
    t.reveal_type(my_parser.parse)
    t.reveal_type(my_parser.__call__)


if __name__ == "__main__":
    main()
