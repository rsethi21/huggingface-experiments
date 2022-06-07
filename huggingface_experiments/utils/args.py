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
        help="The API Access Token of admin of the Organization",
    )
    parser.add_argument(
        "--write-token",
        type=str,
        required=True,
        help="The API Access Token of a user with write permissions for an Organization",
    )
    parser.add_argument(
        "--read-token",
        type=str,
        required=True,
        help="The API Access Token of a user with read permissions for an Organization",
    )
    return parser.parse_args()
