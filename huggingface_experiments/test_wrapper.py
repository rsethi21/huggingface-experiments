from argparse import Namespace
from huggingface_experiments.utils.args import apiArgs

from huggingface_hub import delete_repo, create_repo, update_repo_visibility, upload_file, move_repo, whoami
from requests.exceptions import HTTPError


def _verboseDelete(
    organization: str, repository: str, token: str, username: str
) -> None:
    print(f"===\nDeleting {organization}/{repository} with {username}")
    try:
        delete_repo(repo_id=f"{organization}/{repository}", token=token)
    except HTTPError:
        print("404 Error")


def _verboseCreateRepo(
    organization: str, repository: str, tokenList: list, usernameList: list
) -> None:
    print(f"===\nCreating {organization}/{repository} with {', '.join(usernameList)}")
    adminCreate: str = create_repo(repo_id=f"{organization}/{repository}", token=tokenList[0])
    writeCreate: str = create_repo(repo_id=f"{organization}/{repository}", token=tokenList[1])
    readCreate: str = create_repo(repo_id=f"{organization}/{repository}", token=tokenList[2])
    print(f"Status code results: {[adminCreate, writeCreate, readCreate]}")


def _verboseSetPrivate(
    organization: str, repository: str, token: str, username: str
) -> None:
    print(f"===\nSetting private {organization}/{repository} with {username}")
    private: dict = update_repo_visibility(repo_id=f"{organization}/{repository}", private=True, token=token)
    print(f"Status code result: {[private]}")


def _verboseSetPublic(
    organization: str, repository: str, tokenList: list, usernameList: str
) -> None:
    print(
        f"===\nSetting public {organization}/{repository} with {', '.join(usernameList)}"
    )
    adminPublic: dict = update_repo_visibility(repo_id=f"{organization}/{repository}", private=False, token=tokenList[0])
    writePublic: dict = update_repo_visibility(repo_id=f"{organization}/{repository}", private=False, token=tokenList[1])
    readPublic: dict = update_repo_visibility(repo_id=f"{organization}/{repository}", private=False, token=tokenList[2])
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
    adminCommit: str = upload_file(path_or_fileobj="test/adminTest.txt", path_in_repo=".", repo_id=f"{organization}/{repository}", token=tokenList[0])
    writeCommit: str = upload_file(path_or_fileobj="test/writeTest.txt", path_in_repo=".", repo_id=f"{organization}/{repository}", token=tokenList[0])
    readCommit: str = upload_file(path_or_fileobj="test/readTest.txt", path_in_repo=".", repo_id=f"{organization}/{repository}", token=tokenList[0])
    print(f"Status code results: {[adminCommit, writeCommit, readCommit]}")


def _verboseMove(token: str, username: str, fromRepo: str, toRepo: str) -> None:
    print(
        f"===\nMoving repository from {fromRepo} to {toRepo} with {username}"
    )
    move_repo(from_id=fromRepo, to_id=toRepo, token=token)


def test(
    tokenList: list, usernameList: list, repository: str, movedRepository: str, organization: str = None
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
    _verboseDelete(
        organization=organization,
        repository=movedRepository,
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

    _verboseMove(
        token=tokenList[2],
        username=usernameList[2],
        fromRepo=f"{organization}/{repository}",
        toRepo=f"{organization}/{movedRepository}",
    )  # Read

    _verboseMove(
        token=tokenList[1],
        username=usernameList[1],
        fromRepo=f"{organization}/{repository}",
        toRepo=f"{organization}/{movedRepository}",
    )  # Write

    _verboseMove(
        token=tokenList[0],
        username=usernameList[0],
        fromRepo=f"{organization}/{repository}",
        toRepo=f"{organization}/{movedRepository}",
    )  # Read

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
    )  # Admin


def main() -> None:
    args: Namespace = apiArgs()
    repository: str = args.repository
    movedRepository: str = args.moved_repository
    organization: str = args.organization
    tokenList: list = [args.admin_token, args.write_token, args.read_token]

    print("Retrieving account information from tokens...")
    adminUsername: str = whoami(token=args.admin_token)["name"]
    writeUsername: str = whoami(token=args.write_token)["name"]
    readUsername: str = whoami(token=args.read_token)["name"]

    usernameList: list = [adminUsername, writeUsername, readUsername]

    test(tokenList=tokenList, usernameList=usernameList, repository=repository, movedRepository=movedRepository)
    test(
        tokenList=tokenList,
        usernameList=usernameList,
        repository=repository,
        movedRepository=movedRepository,
        organization=organization,
    )


if __name__ == "__main__":
    main()
