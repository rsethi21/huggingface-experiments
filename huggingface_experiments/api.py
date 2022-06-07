import json
from argparse import Namespace
from email.policy import default

from requests import post
from requests.models import Response
from utils.args import apiArgs

rootURL: str = "https://huggingface.co"


def createModelRepo(token: str, name: str, organization: str = None) -> int:
    url: str = f"{rootURL}/api/repos/create"
    headers: dict = {"authorization": f"Bearer {token}"}

    match organization:
        case None:
            json: dict = {"name": name}
        case _:
            json: dict = {"name": name, "organization": organization}

    p: Response = post(url, headers=headers, json=json)
    return p.content


def main() -> None:
    args: Namespace = apiArgs()
    print(createModelRepo(token=args.admin_token, name="test2"))


if __name__ == "__main__":
    main()
