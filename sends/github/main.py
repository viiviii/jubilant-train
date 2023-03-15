import os

import env
from sends.github.issue import Issue, create


def inputs() -> Issue:
    return env.to_issue()


def outputs(response: dict[str, str]) -> None:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'number={response["number"]}', file=fh)


def send(issue: Issue) -> None:
    response = create(issue)
    outputs(response)


if __name__ == '__main__':
    send(inputs())
