from pathlib import Path

from requests import delete, post, put
from requests.models import Response

rootURL: str = "https://huggingface.co"


def createModelRepo(token: str, name: str, organization: str = None) -> Response:
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
    token: str, name: str, organization: str, private: bool = True
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
    token: str, filepath: str, name: str, organization: str, revision: str = "1"
) -> Response:
    path: Path = Path(filepath)

    url: str = (
        f"{rootURL}/api/model/{name}/{organization}/upload/{revision}/{path.name}"
    )
    headers: dict = {"authorization": f"Bearer {token}"}
    with open(filepath, "rb") as bytesFile:
        u: Response = post(url, data=bytesFile.raw, headers=headers)
        bytesFile.close()
    return u


def deleteModelRepo(token: str, name: str, organization: str) -> Response:
    url: str = f"{rootURL}/api/repos/delete"
    headers: dict = {"authorization": f"Bearer {token}"}
    json: dict = {"name": name, "organization": organization}
    d: Response = delete(url, headers=headers, json=json)
    return d
