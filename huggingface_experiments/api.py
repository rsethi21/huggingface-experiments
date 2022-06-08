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
