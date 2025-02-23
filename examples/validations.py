from __future__ import annotations

import re
import typing as t

from typing_extensions import override

import v6e as v

# --- DEMO UTILS ---
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
DEFAULT = "\033[39m"


def print_title(x: str) -> None:
    print(BLUE + "\n" + x + DEFAULT)


def print_example(prompt: str, result: bool) -> None:
    color = GREEN if result else RED
    print(prompt, color + str(result) + DEFAULT)


# --- DEMO ---
def main() -> None:
    # Basic usage
    can_drink = v.int().gte(21)
    print_title("Basic - Age")
    print_example("With age 21 can you drink?", can_drink.check(21))
    print_example("With age 20 can you drink?", can_drink.check(20))

    # You can "AND" multiple validations
    interview_channel = v.str().starts_with("#").regex("interview.*[0-9]{2}-[0-9]{2}")
    print_title("AND Validations - Slack Channel")
    print_example(
        "Is channel #interview-foo-feb-01-12 an interview slack channel?",
        interview_channel.check("#interview-foo-feb-01-12"),
    )
    print_example(
        "Is channel #foo-feb-01-12 an interview slack channel?",
        interview_channel.check("#foo-feb-01-12"),
    )

    # You can create your own custom validations
    def _validate_earth_age(x: int) -> None:
        if x != 4_543_000_000:
            raise ValueError("The Earth is 4.543 billion years old. Try 4543000000.")

    earth_age = v.int().custom(_validate_earth_age)
    print_title("Custom Validation - Earth Age")
    print_example("Is 4.543 billion years a valid Earth age?", earth_age(4_543_000_000))
    print_example("Is 4.543 million years a valid Earth age?", earth_age(4_543_000))

    # You can create your own reusable validation types or extend existing ones
    class SlackChannel(v.V6eStr):
        @override
        def _parse(self, raw: t.Any) -> str:
            if not isinstance(raw, str):
                raise ValueError(f"Value {raw!r} is not a valid slack channel")

            if re.search("^#[a-z0-9-]$", raw) is None:
                raise v.ValidationException(
                    "Slack channels must start with '#' and contain only letters, numbers, and dashes"
                )

            return raw

    foo_slack_channel = SlackChannel().contains("foo")
    print_title("Reusable Validation Type - Slack Channel")
    print_example(
        "Is #foo-bar a valid slack channel?", foo_slack_channel.check("#foo-bar")
    )
    print_example(
        "Is foo-bar a valid slack channel?", foo_slack_channel.check("foo-bar")
    )

    # Type checking example
    my_validation = v.int().gte(8).lte(4)
    t.reveal_type(my_validation)
    t.reveal_type(my_validation.check)
    t.reveal_type(my_validation.safe_parse)
    t.reveal_type(my_validation.parse)


if __name__ == "__main__":
    main()
