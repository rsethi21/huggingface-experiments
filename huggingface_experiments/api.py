from argparse import Namespace
from getpass import getpass
from pathlib import Path

from requests import delete, get, post, put
from requests.models import Response
from huggingface_experiments.utils.args import apiArgs

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


def uploadFileToModelRepo(
    token: str, filepath: str, organization: str, name: str, revision: str = "main", pullRequest: bool = False
) -> Response:
    path: Path = Path(filepath)

    if pullRequest:
        url: str = f"{rootURL}/api/{organization}/{name}/upload/{revision}/{path.name}?create_pr=1"
    else:
        url: str = f"{rootURL}/api/{organization}/{name}/upload/{revision}/{path.name}"
    headers: dict = {"authorization": f"Bearer {token}"}
    with open(filepath, "rb") as bytesFile:
        c: Response = post(url, data=bytesFile.raw, headers=headers)
        bytesFile.close()
    return c


def deleteModelRepo(token: str, organization: str, name: str) -> Response:
    url: str = f"{rootURL}/api/repos/delete"
    headers: dict = {"authorization": f"Bearer {token}"}
    json: dict = {"name": name, "organization": organization}
    d: Response = delete(url, headers=headers, json=json)
    return d


def _verboseDelete(organization: str, repository: str, token: str, username: str)  ->  None:
    print(f"===\nDeleting {organization}/{repository} with {username}")
    deleteModelRepo(
        token=token, organization=organization, name=repository
    )


def _verboseCreateRepo(organization: str, repository: str, tokenList: list, usernameList: list)    ->  None:
    print(
        f"===\nCreating {organization}/{repository} with {', '.join(usernameList)}"
    )
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

def _verboseSetPrivate(organization: str, repository: str, token: str, username: str)   ->  None:
    print(f"===\nSetting private {organization}/{repository} with {username}")
    private: int = makePrivateModelRepo(
        token=token,
        organization=organization,
        name=repository,
        private=True,
    ).status_code
    print(f"Status code result: {[private]}")


def _verboseSetPublic(organization: str, repository: str, tokenList: list, usernameList: str)   ->  None:
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


def _verboseUpload(organization: str, repository: str, tokenList: list, usernameList: list, pullRequest: bool = False) ->  None:
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

def testUser(tokenList: list, usernameList: list, repository:str) -> None:
    adminUsername: str = usernameList[0]
    writeUsername: str = usernameList[1]
    readUsername: str = usernameList[2]

    adminToken: str = tokenList[0]
    writeToken: str = tokenList[1]
    readToken: str = tokenList[2]

    _verboseDelete(organization=adminUsername, repository=repository, token=adminToken, username=adminUsername)

    _verboseCreateRepo(organization=adminUsername, repository=repository, tokenList=tokenList, usernameList=usernameList)

    _verboseSetPrivate(organization=adminUsername, repository=repository, token=readToken, username=readUsername) # Read

    _verboseSetPrivate(organization=adminUsername, repository=repository, token=writeToken, username=writeUsername) # Write

    _verboseSetPrivate(organization=adminUsername, repository=repository, token=adminToken, username=adminUsername) # Admin

    _verboseSetPublic(organization=adminUsername, repository=repository, tokenList=tokenList, usernameList=usernameList)

    _verboseUpload(organization=adminUsername, repository=repository, tokenList=tokenList, usernameList=usernameList)

    _verboseUpload(organization=adminUsername, repository=repository, tokenList=tokenList, usernameList=usernameList, pullRequest=True)


# def testOrganization(tokenList: list, usernameList: list, organization: str, repository:str) -> None:
#     adminUsername: str = usernameList[0]

#     adminToken: str = tokenList[0]
#     writeToken: str = tokenList[0]
#     readToken: str = tokenList[0]

#     print(f"===\nDeleting {organization}/{repository} with {adminUsername}")
#     deleteModelRepo(
#         token=adminToken, organization=organization, name=repository
#     )

#     print(
#         f"===\nCreating {organization}/{repository} with {', '.join(usernameList)}"
#     )
#     adminCreate: int = createModelRepo(
#         token=adminToken, organization=organization, name=repository
#     ).status_code
#     writeCreate: int = createModelRepo(
#         token=writeToken, organization=organization, name=repository
#     ).status_code
#     readCreate: int = createModelRepo(
#         token=readToken, organization=organization, name=repository
#     ).status_code
#     print(f"Status code results: {[adminCreate, writeCreate, readCreate]}")

#     print(
#         f"===\nSetting private {organization}/{repository} with {', '.join(usernameList)}"
#     )
#     adminPrivate: int = makePrivateModelRepo(
#         token=adminToken,
#         organization=organization,
#         name=repository,
#         private=True,
#     ).status_code
#     writePrivate: int = makePrivateModelRepo(
#         token=writeToken,
#         organization=organization,
#         name=repository,
#         private=True,
#     ).status_code
#     readPrivate: int = makePrivateModelRepo(
#         token=readToken,
#         organization=organization,
#         name=repository,
#         private=True,
#     ).status_code
#     print(f"Status code results: {[adminPrivate, writePrivate, readPrivate]}")

#     print(
#         f"===\nSetting public {organization}/{repository} with {', '.join(usernameList)}"
#     )
#     adminPublic: int = makePrivateModelRepo(
#         token=adminToken,
#         organization=organization,
#         name=repository,
#         private=False,
#     ).status_code
#     writePublic: int = makePrivateModelRepo(
#         token=writeToken,
#         organization=organization,
#         name=repository,
#         private=False,
#     ).status_code
#     readPublic: int = makePrivateModelRepo(
#         token=readToken,
#         organization=organization,
#         name=repository,
#         private=False,
#     ).status_code
#     print(f"Status code results: {[adminPublic, writePublic, readPublic]}")

#     print(
#         f"===\nCommitting file to {organization}/{repository} with {', '.join(usernameList)}"
#     )
#     adminCommit: int = commitFileToModelRepo(
#         token=adminToken,
#         organization=organization,
#         name=repository,
#         filepath="test/adminTest.txt",
#     ).status_code
#     writeCommit: int = commitFileToModelRepo(
#         token=writeToken,
#         filepath="test/writeTest.txt",
#         organization=organization,
#         name=repository,
#     ).status_code
#     readCommit: int = commitFileToModelRepo(
#         token=readToken,
#         filepath="test/readTest.txt",
#         organization=organization,
#         name=repository,
#     ).status_code
#     print(f"Status code results: {[adminCommit, writeCommit, readCommit]}")

#     print(
#         f"===\nCreating a Pull Request for a file to {organization}/{repository} with {', '.join(usernameList)}"
#     )
#     adminPullRequest: int = pullRequestFileToModelRepo(
#         token=adminToken,
#         organization=organization,
#         name=repository,
#         filepath="test/adminTest.txt",
#     ).status_code
#     writePullRequest: int = pullRequestFileToModelRepo(
#         token=writeToken,
#         filepath="test/writeTest.txt",
#         organization=organization,
#         name=repository,
#     ).status_code
#     readPullRequest: int = pullRequestFileToModelRepo(
#         token=readToken,
#         filepath="test/readTest.txt",
#         organization=organization,
#         name=repository,
#     ).status_code
#     print(f"Status code results: {[adminPullRequest, writePullRequest, readPullRequest]}")

#     getpass(f"Press ENTER to delete {organization}/{repository}")
#     print(f"===\nDeleting {organization}/{repository} with {adminUsername}")
#     deleteModelRepo(
#         token=adminToken, organization=organization, name=repository
#     )


def main() -> None:
    args: Namespace = apiArgs()
    repository: str = args.repo_name
    tokenList: list = [args.admin_token, args.write_token, args.read_token]

    print("Retrieving account information from tokens...")
    adminUsername: str = whoAmI(token=args.admin_token).json()["name"]
    writeUsername: str = whoAmI(token=args.write_token).json()["name"]
    readUsername: str = whoAmI(token=args.read_token).json()["name"]

    usernameList: list = [adminUsername, writeUsername, readUsername]


    testUser(tokenList=tokenList, usernameList=usernameList, repository=repository)
    # testOrganization()


if __name__ == "__main__":
    main()
