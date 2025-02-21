from __future__ import annotations

from typing import Callable, reveal_type

import v6e

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
    can_drink = v6e.Gte(21)
    print_title("Basic - Age")
    print_example("With age 21 can you drink?", can_drink(21))
    print_example("With age 20 can you drink?", can_drink(20))

    # You can "AND" multiple validations
    interview_channel = v6e.StartsWith("#") & v6e.ReSearch(
        "interview.*[0-9]{2}-[0-9]{2}"
    )
    print_title("AND Validations - Slack Channel")
    print_example(
        "Is channel #interview-foo-feb-01-12 an interview slack channel?",
        interview_channel("#interview-foo-feb-01-12"),
    )
    print_example(
        "Is channel #foo-feb-01-12 an interview slack channel?",
        interview_channel("#foo-feb-01-12"),
    )

    # You can "OR" multiple validations
    slack_or_jira = v6e.ReMatch(r"#[a-z0-9-]+") | v6e.ReMatch(r"[A-Z0-9_]+")
    print_title("OR Validations - Slack or Jira")
    print_example("Is #foo-bar-1 a valid slack or Jira?", slack_or_jira("#foo-bar-1"))
    print_example("Is FOO_BAR100 a valid slack or Jira?", slack_or_jira("FOO_BAR100"))
    print_example("Is foo-bar-1 a valid slack or Jira?", slack_or_jira("foo-bar-1"))

    # You can create your own custom validations
    def _validate_earth_age(x: int) -> None:
        if x != 4_543_000_000:
            raise ValueError("The Earth is 4.543 billion years old. Try 4543000000.")

    earth_age = v6e.Custom(_validate_earth_age)
    print_title("Custom Validation - Earth Age")
    print_example("Is 4.543 billion years a valid Earth age?", earth_age(4_543_000_000))
    print_example("Is 4.543 million years a valid Earth age?", earth_age(4_543_000))

    # You can create your own reusable validation types
    class SlackChannel(v6e.Validation[str]):
        def rule(self, x: str):
            if not x.startswith("#"):
                raise v6e.ValidationException("Slack channels must start with '#'")

    slack_channel = SlackChannel()
    print_title("Reusable Validation Type - Slack Channel")
    print_example("Is #foo-bar a valid slack channel?", slack_channel("#foo-bar"))
    print_example("Is foo-bar a valid slack channel?", slack_channel("foo-bar"))

    # Type checking example
    def prompt(msg: str, validate: Callable[[int], bool]):
        res: int = int(input(YELLOW + msg + DEFAULT))
        if not validate(res):
            print("Whoops! Invalid response")
            return prompt(msg, validate)
        return res

    my_validation = v6e.Gte(8) | v6e.Lte(4)
    reveal_type(my_validation)
    print_title("Type checking example")
    prompt("<4 or >8, please: ", my_validation)


if __name__ == "__main__":
    main()
