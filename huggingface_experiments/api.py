import json
from argparse import Namespace
from email.policy import default

from requests import delete, post
from requests.models import Response
from utils.args import apiArgs

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


def deleteModelRepo(token: str, name: str, organization: str = None) -> Response:
    url: str = f"{rootURL}/api/repos/delete"
    headers: dict = {"authorization": f"Bearer {token}"}

    match organization:
        case None:
            json: dict = {"name": name}
        case _:
            json: dict = {"name": name, "organization": organization}

    d: Response = delete(url, headers=headers, json=json)
    return d


def main() -> None:
    args: Namespace = apiArgs()
    print(createModelRepo(token=args.admin_token, name="test1").content)
    print(
        deleteModelRepo(
            token=args.admin_token, name="test1", organization="NicholasSynovic"
        ).content
    )


if __name__ == "__main__":
    main()
