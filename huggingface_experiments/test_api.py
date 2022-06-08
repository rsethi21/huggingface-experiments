from argparse import Namespace

from huggingface_experiments.api import *


def _verboseDelete(
    organization: str, repository: str, token: str, username: str
) -> None:
    print(f"===\nDeleting {organization}/{repository} with {username}")
    delete: int = deleteModelRepo(
        token=token, organization=organization, name=repository
    ).status_code
    print(f"Status code results: {[delete]}")


def _verboseCreateRepo(
    organization: str, repository: str, tokenList: list, usernameList: list
) -> None:
    print(f"===\nCreating {organization}/{repository} with {', '.join(usernameList)}")
    adminCreate: int = createModelRepo(
        token=tokenList[0], organization=organization, name=repository
    ).status_code
    writeCreate: int = createModelRepo(
        token=tokenList[1], organization=organization, name=repository
    ).status_code
    readCreate: int = createModelRepo(
        token=tokenList[2], organization=organization, name=repository
    ).status_code
    print(f"Status code results: {[adminCreate, writeCreate, readCreate]}")


def _verboseSetPrivate(
    organization: str, repository: str, token: str, username: str
) -> None:
    print(f"===\nSetting private {organization}/{repository} with {username}")
    private: int = makePrivateModelRepo(
        token=token,
        organization=organization,
        name=repository,
        private=True,
    ).status_code
    print(f"Status code result: {[private]}")


def _verboseSetPublic(
    organization: str, repository: str, tokenList: list, usernameList: str
) -> None:
    print(
        f"===\nSetting public {organization}/{repository} with {', '.join(usernameList)}"
    )
    adminPublic: int = makePrivateModelRepo(
        token=tokenList[0],
        organization=organization,
        name=repository,
        private=False,
    ).status_code
    writePublic: int = makePrivateModelRepo(
        token=tokenList[1],
        organization=organization,
        name=repository,
        private=False,
    ).status_code
    readPublic: int = makePrivateModelRepo(
        token=tokenList[2],
        organization=organization,
        name=repository,
        private=False,
    ).status_code
    print(f"Status code results: {[adminPublic, writePublic, readPublic]}")


def _verboseUpload(
    organization: str,
    repository: str,
    tokenList: list,
    usernameList: list,
    pullRequest: bool = False,
) -> None:
    if pullRequest:
        print(
            f"===\nCreating a pull request for a file to {organization}/{repository} with {', '.join(usernameList)}"
        )
    else:
        print(
            f"===\nCommitting file to {organization}/{repository} with {', '.join(usernameList)}"
        )
    adminCommit: int = uploadFileToModelRepo(
        token=tokenList[0],
        organization=organization,
        name=repository,
        filepath="test/adminTest.txt",
        pullRequest=pullRequest,
    ).status_code
    writeCommit: int = uploadFileToModelRepo(
        token=tokenList[1],
        filepath="test/writeTest.txt",
        organization=organization,
        name=repository,
        pullRequest=pullRequest,
    ).status_code
    readCommit: int = uploadFileToModelRepo(
        token=tokenList[2],
        filepath="test/readTest.txt",
        organization=organization,
        name=repository,
        pullRequest=pullRequest,
    ).status_code
    print(f"Status code results: {[adminCommit, writeCommit, readCommit]}")


def test(
    tokenList: list, usernameList: list, repository: str, organization: str = None
) -> None:
    adminUsername: str = usernameList[0]
    writeUsername: str = usernameList[1]
    readUsername: str = usernameList[2]

    adminToken: str = tokenList[0]
    writeToken: str = tokenList[1]
    readToken: str = tokenList[2]

    if organization is None:
        organization = adminUsername

    _verboseDelete(
        organization=organization,
        repository=repository,
        token=adminToken,
        username=adminUsername,
    )

    _verboseCreateRepo(
        organization=organization,
        repository=repository,
        tokenList=tokenList,
        usernameList=usernameList,
    )

    _verboseSetPrivate(
        organization=organization,
        repository=repository,
        token=readToken,
        username=readUsername,
    )  # Read

    _verboseSetPrivate(
        organization=organization,
        repository=repository,
        token=writeToken,
        username=writeUsername,
    )  # Write

    _verboseSetPrivate(
        organization=organization,
        repository=repository,
        token=adminToken,
        username=adminUsername,
    )  # Admin

    _verboseSetPublic(
        organization=organization,
        repository=repository,
        tokenList=tokenList,
        usernameList=usernameList,
    )

    _verboseUpload(
        organization=organization,
        repository=repository,
        tokenList=tokenList,
        usernameList=usernameList,
    )

    _verboseUpload(
        organization=organization,
        repository=repository,
        tokenList=tokenList,
        usernameList=usernameList,
        pullRequest=True,
    )

    _verboseDelete(
        organization=organization,
        repository=repository,
        token=tokenList[2],
        username=usernameList[2],
    )  # Read

    _verboseDelete(
        organization=organization,
        repository=repository,
        token=tokenList[1],
        username=usernameList[1],
    )  # Write

    _verboseDelete(
        organization=organization,
        repository=repository,
        token=tokenList[0],
        username=usernameList[0],
    )  # Read


def main() -> None:
    args: Namespace = apiArgs()
    repository: str = args.repo_name
    organization: str = args.organization
    tokenList: list = [args.admin_token, args.write_token, args.read_token]

    print("Retrieving account information from tokens...")
    adminUsername: str = whoAmI(token=args.admin_token).json()["name"]
    writeUsername: str = whoAmI(token=args.write_token).json()["name"]
    readUsername: str = whoAmI(token=args.read_token).json()["name"]

    usernameList: list = [adminUsername, writeUsername, readUsername]

    test(tokenList=tokenList, usernameList=usernameList, repository=repository)
    test(
        tokenList=tokenList,
        usernameList=usernameList,
        repository=repository,
        organization=organization,
    )


if __name__ == "__main__":
    main()
