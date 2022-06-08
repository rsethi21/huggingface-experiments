from huggingface_experiments.utils.args import searchArgs
from argparse import Namespace
from typing import List

from huggingface_hub import list_models
from huggingface_hub.hf_api import ModelInfo
from progress.bar import Bar


def search(token: str) -> List[ModelInfo]:
    print("Getting all models from HuggingFace.co...")
    return list_models(
        full=True, cardData=True, fetch_config=True, use_auth_token=token
    )


def main() -> None:
    args: Namespace = searchArgs()
    results: List[ModelInfo] = search(token=args.token)
    with open(args.output, "w") as output:
        with Bar(f"Writing data to {args.output}...", max=len(results)) as bar:
            model: ModelInfo
            for model in results:
                output.write(f"https://huggingface.co/{model.modelId}\n")
                bar.next()
        output.close()


if __name__ == "__main__":
    main()
