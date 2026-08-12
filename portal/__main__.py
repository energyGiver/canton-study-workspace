from __future__ import annotations

import argparse

from .build import build_site


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Build and run the Canton research portal")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("build", help="Compose the ignored local Mintlify site")
    return root


def main() -> None:
    args = parser().parse_args()
    if args.command == "build":
        result = build_site()
        print(f"Built {result.site_dir} from cf-docs {result.upstream_commit[:12]}")


if __name__ == "__main__":
    main()
