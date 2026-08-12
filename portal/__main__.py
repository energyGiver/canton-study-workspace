from __future__ import annotations

import argparse
import json
import subprocess
import threading
from pathlib import Path

from .build import build_site, refresh_translations
from .content import ContentRepository
from .inventory import TranslationPolicy, official_navigation_paths
from .server import PortalApplication, serve
from .sync import sync_upstream
from .validate import validate_workspace


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Build and run the Canton research portal")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("build", help="Compose the ignored local Mintlify site")
    commands.add_parser(
        "refresh", help="Refresh translations in an active local preview"
    )
    serve_command = commands.add_parser("serve", help="Run the local research API")
    serve_command.add_argument("--host", default="127.0.0.1")
    serve_command.add_argument("--port", type=int, default=8787)
    serve_command.add_argument("--no-index", action="store_true")

    commands.add_parser("index", help="Rebuild the local full-text search index")
    sync_command = commands.add_parser("sync", help="Check or apply official docs updates")
    sync_command.add_argument("--update", action="store_true")
    commands.add_parser("validate", help="Validate shared research metadata and source hashes")
    translations_command = commands.add_parser(
        "translations", help="Show the current Korean translation backlog"
    )
    translations_command.add_argument(
        "--output", default=".generated/translation-backlog.json"
    )

    dev_command = commands.add_parser("dev", help="Run the research API and Mintlify")
    dev_command.add_argument("--api-port", type=int, default=8787)
    dev_command.add_argument("--docs-port", type=int, default=3000)
    return root


def main() -> None:
    args = parser().parse_args()
    if args.command == "build":
        result = build_site()
        print(f"Built {result.site_dir} from cf-docs {result.upstream_commit[:12]}")
    elif args.command == "refresh":
        count = refresh_translations()
        print(f"Refreshed {count} translations without stopping the local preview")
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
        print(
            "Upstream changes ignored by the local translation policy: "
            f"{len(report.ignored_changed_files)}"
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
    elif args.command == "translations":
        repository = ContentRepository()
        policy = TranslationPolicy()
        official_order = official_navigation_paths()
        official_paths = set(official_order)
        translated = {
            page.path
            for page in repository.pages
            if page.path in official_paths and repository.translation(page)["available"]
        }
        excluded = official_paths & set(policy.by_path)
        backlog = [
            path
            for path in official_order
            if path not in translated and path not in excluded
        ]
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output = {
            "official_file_backed_navigation_pages": len(official_paths),
            "korean_translations": len(translated),
            "locally_excluded": len(excluded),
            "translation_backlog": len(backlog),
            "items": [
                {
                    "path": path,
                    "title": repository.by_path[path].title,
                    "source_bytes": repository.official_source_path(
                        repository.by_path[path]
                    ).stat().st_size,
                }
                for path in backlog
            ],
        }
        output_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Official file-backed navigation pages: {len(official_paths)}")
        print(f"Korean translations: {len(translated)}")
        print(f"Locally excluded from translation tracking: {len(excluded)}")
        print(f"Translation backlog: {len(backlog)}")
        print(f"Backlog file: {output_path}")
        for path in backlog:
            print(path)
    elif args.command == "dev":
        validation = validate_workspace()
        for warning in validation.warnings:
            print(f"WARNING: {warning}")
        for error in validation.errors:
            print(f"ERROR: {error}")
        if not validation.valid:
            raise SystemExit("Workspace validation failed; local preview was not started")
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
                "mintlify@4.2.796",
                "dev",
                "--port",
                str(args.docs_port),
            ],
            cwd=result.site_dir,
            check=True,
        )


if __name__ == "__main__":
    main()
