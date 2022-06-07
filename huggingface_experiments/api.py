from argparse import Namespace
from getpass import getpass
from pathlib import Path

from requests import delete, get, post, put
from requests.models import Response
from utils.args import apiArgs

rootURL: str = "https://huggingface.co"


def whoAmI(token: str) -> Response:
    url: str = f"{rootURL}/api/whoami-v2"
    headers: dict = {"authorization": f"Bearer {token}"}
    w: Response = get(url, headers=headers)
    return w


def createModelRepo(token: str, organization: str, name: str) -> Response:
    url: str = f"{rootURL}/api/repos/create"
    headers: dict = {"authorization": f"Bearer {token}"}

    match organization:
        case None:
            json: dict = {"name": name}
        case _:
            json: dict = {"name": name, "organization": organization}

    p: Response = post(url, headers=headers, json=json)
    return p


def makePrivateModelRepo(
    token: str, organization: str, name: str, private: bool = True
) -> Response:
    url: str = f"{rootURL}/api/{organization}/{name}/settings"
    headers: dict = {"authorization": f"Bearer {token}"}
    json: dict = {"private": private}
    mp: Response = put(url, headers=headers, json=json)
    return mp


def moveModelRepo(token: str, fromRepo: str, toRepo: str) -> Response:
    url: str = f"{rootURL}/api/repos/move"
    headers: dict = {"authorization": f"Bearer {token}"}
    json: dict = {"fromRepo": fromRepo, "toRepo": toRepo}
    m: Response = post(url, headers=headers, json=json)
    return m


def commitFileToModelRepo(
    token: str, filepath: str, organization: str, name: str, revision: str = "main"
) -> Response:
    path: Path = Path(filepath)

    url: str = f"{rootURL}/api/{organization}/{name}/upload/{revision}/{path.name}"
    headers: dict = {"authorization": f"Bearer {token}"}
    with open(filepath, "rb") as bytesFile:
        c: Response = post(url, data=bytesFile.raw, headers=headers)
        bytesFile.close()
    return c


def pullRequestFileToModelRepo(
    token: str, filepath: str, organization: str, name: str, revision: str = "main"
) -> Response:
    path: Path = Path(filepath)

    url: str = (
        f"{rootURL}/api/{organization}/{name}/upload/{revision}/{path.name}?create_pr=1"
    )
    headers: dict = {"authorization": f"Bearer {token}"}
    with open(filepath, "rb") as bytesFile:
        pr: Response = post(url, data=bytesFile.raw, headers=headers)
        bytesFile.close()
    return pr


def deleteModelRepo(token: str, organization: str, name: str) -> Response:
    url: str = f"{rootURL}/api/repos/delete"
    headers: dict = {"authorization": f"Bearer {token}"}
    json: dict = {"name": name, "organization": organization}
    d: Response = delete(url, headers=headers, json=json)
    return d


def testUser() -> None:
    args: Namespace = apiArgs()
    print("Testing the HuggableFace.co REST API...\n===")
    print("Retrieving account information from tokens...")
    adminUsername: str = whoAmI(token=args.admin_token).json()["name"]
    writeUsername: str = whoAmI(token=args.write_token).json()["name"]
    readUsername: str = whoAmI(token=args.read_token).json()["name"]
    accountList: list = [writeUsername, readUsername]
    accountList_Admin: list = [adminUsername, writeUsername, readUsername]

    print(f"===\nDeleting {args.repo_name} on {adminUsername}")
    deleteModelRepo(
        token=args.admin_token, organization=adminUsername, name=args.repo_name
    )

    print(
        f"===\nCreating {args.repo_name} on {adminUsername} from {', '.join(accountList_Admin)}"
    )
    adminCreate: int = createModelRepo(
        token=args.admin_token, organization=adminUsername, name=args.repo_name
    ).status_code
    writeCreate: int = createModelRepo(
        token=args.write_token, organization=adminUsername, name=args.repo_name
    ).status_code
    readCreate: int = createModelRepo(
        token=args.read_token, organization=adminUsername, name=args.repo_name
    ).status_code
    print(f"Status code results: {[adminCreate, writeCreate, readCreate]}")

    print(
        f"===\nSetting private {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writePrivate: int = makePrivateModelRepo(
        token=args.write_token,
        organization=adminUsername,
        name=args.repo_name,
        private=True,
    ).status_code
    readPrivate: int = makePrivateModelRepo(
        token=args.read_token,
        organization=adminUsername,
        name=args.repo_name,
        private=True,
    ).status_code
    print(f"Status code results: {[writePrivate, readPrivate]}")

    print(
        f"===\nSetting private {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminPrivate: int = makePrivateModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        private=True,
    ).status_code
    print(f"Status code result: {[adminPrivate]}")

    print(
        f"===\nSetting public {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writePublic: int = makePrivateModelRepo(
        token=args.write_token,
        organization=adminUsername,
        name=args.repo_name,
        private=False,
    ).status_code
    readPublic: int = makePrivateModelRepo(
        token=args.read_token,
        organization=adminUsername,
        name=args.repo_name,
        private=False,
    ).status_code
    print(f"Status code results: {[writePublic, readPublic]}")

    print(
        f"===\nSetting public {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminPrivate: int = makePrivateModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        private=False,
    ).status_code
    print(f"Status code result: {[adminPrivate]}")

    print(
        f"===\nCommitting file to {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writeCommit: int = commitFileToModelRepo(
        token=args.write_token,
        filepath="test/writeTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    readCommit: int = commitFileToModelRepo(
        token=args.read_token,
        filepath="test/readTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    print(f"Status code results: {[writeCommit, readCommit]}")

    print(
        f"===\nCommitting file to {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminCommit: int = commitFileToModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        filepath="test/adminTest.txt",
    ).status_code
    print(f"Status code result: {[adminCommit]}")

    print(
        f"===\nCreating a Pull Request for a file to {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writePullRequest: int = pullRequestFileToModelRepo(
        token=args.write_token,
        filepath="test/writeTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    readPullRequest: int = pullRequestFileToModelRepo(
        token=args.read_token,
        filepath="test/readTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    print(f"Status code results: {[writePullRequest, readPullRequest]}")

    print(
        f"===\nCreating a Pull Request to {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminPullRequest: int = pullRequestFileToModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        filepath="test/adminTest.txt",
    ).status_code
    print(f"Status code result: {[adminPullRequest]}")

    getpass(f"Press ENTER to delete {args.repo_name}")
    print(f"===\nDeleting {args.repo_name} on {adminUsername}")
    deleteModelRepo(
        token=args.admin_token, organization=adminUsername, name=args.repo_name
    )


def testOrganization() -> None:
    args: Namespace = apiArgs()
    print("Testing the HuggableFace.co REST API...\n===")
    print("Retrieving account information from tokens...")
    adminUsername: str = whoAmI(token=args.admin_token).json()["name"]
    writeUsername: str = whoAmI(token=args.write_token).json()["name"]
    readUsername: str = whoAmI(token=args.read_token).json()["name"]
    accountList: list = [writeUsername, readUsername]
    accountList_Admin: list = [adminUsername, writeUsername, readUsername]

    print(f"===\nDeleting {args.repo_name} on {adminUsername}")
    deleteModelRepo(
        token=args.admin_token, organization=adminUsername, name=args.repo_name
    )

    print(
        f"===\nCreating {args.repo_name} on {adminUsername} from {', '.join(accountList_Admin)}"
    )
    adminCreate: int = createModelRepo(
        token=args.admin_token, organization=adminUsername, name=args.repo_name
    ).status_code
    writeCreate: int = createModelRepo(
        token=args.write_token, organization=adminUsername, name=args.repo_name
    ).status_code
    readCreate: int = createModelRepo(
        token=args.read_token, organization=adminUsername, name=args.repo_name
    ).status_code
    print(f"Status code results: {[adminCreate, writeCreate, readCreate]}")

    print(
        f"===\nSetting private {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writePrivate: int = makePrivateModelRepo(
        token=args.write_token,
        organization=adminUsername,
        name=args.repo_name,
        private=True,
    ).status_code
    readPrivate: int = makePrivateModelRepo(
        token=args.read_token,
        organization=adminUsername,
        name=args.repo_name,
        private=True,
    ).status_code
    print(f"Status code results: {[writePrivate, readPrivate]}")

    print(
        f"===\nSetting private {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminPrivate: int = makePrivateModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        private=True,
    ).status_code
    print(f"Status code result: {[adminPrivate]}")

    print(
        f"===\nSetting public {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writePublic: int = makePrivateModelRepo(
        token=args.write_token,
        organization=adminUsername,
        name=args.repo_name,
        private=False,
    ).status_code
    readPublic: int = makePrivateModelRepo(
        token=args.read_token,
        organization=adminUsername,
        name=args.repo_name,
        private=False,
    ).status_code
    print(f"Status code results: {[writePublic, readPublic]}")

    print(
        f"===\nSetting public {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminPrivate: int = makePrivateModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        private=False,
    ).status_code
    print(f"Status code result: {[adminPrivate]}")

    print(
        f"===\nCommitting file to {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writeCommit: int = commitFileToModelRepo(
        token=args.write_token,
        filepath="test/writeTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    readCommit: int = commitFileToModelRepo(
        token=args.read_token,
        filepath="test/readTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    print(f"Status code results: {[writeCommit, readCommit]}")

    print(
        f"===\nCommitting file to {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminCommit: int = commitFileToModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        filepath="test/adminTest.txt",
    ).status_code
    print(f"Status code result: {[adminCommit]}")

    print(
        f"===\nCreating a Pull Request for a file to {args.repo_name} on {adminUsername} from {', '.join(accountList)}"
    )
    writePullRequest: int = pullRequestFileToModelRepo(
        token=args.write_token,
        filepath="test/writeTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    readPullRequest: int = pullRequestFileToModelRepo(
        token=args.read_token,
        filepath="test/readTest.txt",
        organization=adminUsername,
        name=args.repo_name,
    ).status_code
    print(f"Status code results: {[writePullRequest, readPullRequest]}")

    print(
        f"===\nCreating a Pull Request to {args.repo_name} on {adminUsername} from {adminUsername}"
    )
    adminPullRequest: int = pullRequestFileToModelRepo(
        token=args.admin_token,
        organization=adminUsername,
        name=args.repo_name,
        filepath="test/adminTest.txt",
    ).status_code
    print(f"Status code result: {[adminPullRequest]}")

    getpass(f"Press ENTER to delete {args.repo_name}")
    print(f"===\nDeleting {args.repo_name} on {adminUsername}")
    deleteModelRepo(
        token=args.admin_token, organization=adminUsername, name=args.repo_name
    )


def main() -> None:
    testUser()
    testOrganization()


if __name__ == "__main__":
    main()
