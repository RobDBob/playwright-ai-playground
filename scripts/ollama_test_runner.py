import argparse
import os
import subprocess
import sys
from pathlib import Path

from ollama import chat


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run pytest and summarize its output with a local Ollama model."
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OLLAMA_MODEL", "llama3.2"),
        help="Installed local Ollama model (default: OLLAMA_MODEL or llama3.2).",
    )
    args, pytest_args = parser.parse_known_args()

    project_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *pytest_args],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    test_output = (result.stdout + "\n" + result.stderr)[-12000:]
    response = chat(
        model=args.model,
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarize this pytest run. State the outcome, failures if any, "
                    "and the most useful next step. Do not invent details.\n\n"
                    f"{test_output}"
                ),
            }
        ],
    )
    print(f"\nOllama summary ({args.model}):")
    print(response.message.content)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
