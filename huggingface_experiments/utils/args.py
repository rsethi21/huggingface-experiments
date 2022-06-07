from argparse import ArgumentParser, Namespace

name: str = "HuggingFace.co"
authors: list = ["Nicholas M. Synovic"]


def apiArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} API Experiments",
        usage="Experiments to test the HuggingFace.co REST API",
        epilog=f"Tests written by: {', '.join(authors)}",
    )
    parser.add_argument(
        "--admin-token",
        type=str,
        required=True,
        help="The API Access Token of the/ an admin of the organization",
    )
    parser.add_argument(
        "--write-token",
        type=str,
        required=True,
        help="The API Access Token of a user with write permissions for an organization",
    )
    parser.add_argument(
        "--read-token",
        type=str,
        required=True,
        help="The API Access Token of a user with read permissions for an organization",
    )
    parser.add_argument("--repo-name", type=str, required=False, default="test", help="The name of the test repository to use. NOTE: This is temporary and will be deleted at the end of this experiment.")
    return parser.parse_args()
