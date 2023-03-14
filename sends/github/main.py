import os

from lotto.secret import Secret
from sends.github.issue import Issue, create


class Inputs:
    TOKEN = 'ISSUE_TOKEN'
    REPOSITORY = 'ISSUE_REPOSITORY'
    TITLE = 'ISSUE_TITLE'
    CONTENT = 'ISSUE_CONTENT'
    LABEL = 'ISSUE_LABEL'

    @staticmethod
    def to_issue():
        return Issue(
            token=Secret(os.environ[Inputs.TOKEN]),
            repository=os.environ[Inputs.REPOSITORY],
            title=os.environ[Inputs.TITLE],
            content=os.environ[Inputs.CONTENT],
            label=os.getenv(Inputs.LABEL),
        )


def outputs(response: dict[str, str]) -> None:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'number={response["number"]}', file=fh)


def send(issue: Issue) -> None:
    response = create(issue)
    outputs(response)


if __name__ == '__main__':
    send(Inputs.to_issue())
