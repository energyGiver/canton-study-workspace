from __future__ import annotations

import argparse
import subprocess
import threading

from .build import build_site
from .server import PortalApplication, serve
from .sync import sync_upstream
from .validate import validate_workspace


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Build and run the Canton research portal")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("build", help="Compose the ignored local Mintlify site")
    serve_command = commands.add_parser("serve", help="Run the local research API")
    serve_command.add_argument("--host", default="127.0.0.1")
    serve_command.add_argument("--port", type=int, default=8787)
    serve_command.add_argument("--no-index", action="store_true")

    commands.add_parser("index", help="Rebuild the local full-text search index")
    sync_command = commands.add_parser("sync", help="Check or apply official docs updates")
    sync_command.add_argument("--update", action="store_true")
    commands.add_parser("validate", help="Validate shared research metadata and source hashes")

    dev_command = commands.add_parser("dev", help="Run the research API and Mintlify")
    dev_command.add_argument("--api-port", type=int, default=8787)
    dev_command.add_argument("--docs-port", type=int, default=3000)
    return root


def main() -> None:
    args = parser().parse_args()
    if args.command == "build":
        result = build_site()
        print(f"Built {result.site_dir} from cf-docs {result.upstream_commit[:12]}")
    elif args.command == "serve":
        serve(args.host, args.port, rebuild_index=not args.no_index)
    elif args.command == "index":
        application = PortalApplication(rebuild_index=True)
        print(f"Indexed {application.indexed_documents} documents")
    elif args.command == "sync":
        report = sync_upstream(update=args.update)
        action = "Updated" if report.updated else "Checked"
        print(
            f"{action} cf-docs {report.previous_commit[:12]} -> "
            f"{report.target_commit[:12]} ({len(report.changed_files)} changed files)"
        )
        print(
            f"Stale summaries: {len(report.stale_summaries)}; "
            f"stale translations: {len(report.stale_translations)}"
        )
    elif args.command == "validate":
        report = validate_workspace()
        for warning in report.warnings:
            print(f"WARNING: {warning}")
        for error in report.errors:
            print(f"ERROR: {error}")
        print(
            f"Validated {report.pages} pages, {report.summaries} summaries, "
            f"and {report.translations} translations"
        )
        if not report.valid:
            raise SystemExit(1)
    elif args.command == "dev":
        result = build_site()
        api_thread = threading.Thread(
            target=serve,
            kwargs={"port": args.api_port, "rebuild_index": True},
            daemon=True,
        )
        api_thread.start()
        subprocess.run(
            [
                "npx",
                "-y",
                "mintlify@4.2.595",
                "dev",
                "--port",
                str(args.docs_port),
            ],
            cwd=result.site_dir,
            check=True,
        )


if __name__ == "__main__":
    main()
