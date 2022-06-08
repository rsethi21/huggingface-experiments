from argparse import ArgumentParser, HelpFormatter, Namespace
from operator import attrgetter

name: str = "HuggingFace.co"
authors: list = ["Nicholas M. Synovic"]


class SortingHelpFormatter(HelpFormatter):
    """
    SortingHelpFormatter _summary_
    _extended_summary_
    :param HelpFormatter: _description_
    :type HelpFormatter: _type_
    """

    def add_arguments(self, actions):
        """
        add_arguments _summary_
        _extended_summary_
        :param actions: _description_
        :type actions: _type_
        """
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


def apiArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} API Experiments",
        usage="Experiments to test the HuggingFace.co REST API",
        epilog=f"Tests written by: {', '.join(authors)}",
        formatter_class=SortingHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--admin-token",
        type=str,
        required=True,
        help="The API Access Token of the/ an admin of the organization",
    )
    parser.add_argument(
        "-w",
        "--write-token",
        type=str,
        required=True,
        help="The API Access Token of a user with write permissions for an organization",
    )
    parser.add_argument(
        "-r",
        "--read-token",
        type=str,
        required=True,
        help="The API Access Token of a user with read permissions for an organization",
    )
    parser.add_argument(
        "-n",
        "--repository",
        type=str,
        required=False,
        default="test",
        help="The name of the test repository to use. NOTE: This is temporary and will be deleted at the end of this experiment.",
    )
    parser.add_argument(
        "-m",
        "--moved-repository",
        type=str,
        required=False,
        default="test1",
        help="The name of the test repository after it has been moved. NOTE: This is temporary and will be deleted at the end of this experiment.",
    )
    parser.add_argument(
        "-o",
        "--organization",
        type=str,
        required=True,
        help="The organization to test user access on.",
    )
    return parser.parse_args()
