from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qs, urlparse

from .content import ContentConflictError, ContentRepository
from .store import DraftConflictError, PortalStore


ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT / "data" / "local" / "research.sqlite"
MIGRATIONS_DIR = ROOT / "portal" / "migrations"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def write_origin_allowed(origin: str | None) -> bool:
    if origin is None:
        return True
    parsed = urlparse(origin)
    return parsed.scheme == "http" and parsed.hostname in LOCAL_HOSTS


class PortalApplication:
    def __init__(self, rebuild_index: bool = True) -> None:
        self.content = ContentRepository()
        self.store = PortalStore(DATABASE_PATH, MIGRATIONS_DIR)
        self.indexed_documents = 0
        if rebuild_index:
            self.indexed_documents = self.store.rebuild_search(
                self.content.search_documents()
            )

    def page_payload(self, value: str) -> dict:
        page = self.content.page(value)
        payload = self.content.details(page)
        payload["progress"] = self.store.get_progress(page.source_id)
        payload["favorite"] = self.store.is_favorite(page.source_id)
        payload["draft"] = self.store.get_draft(page.source_id, "summary")
        payload["note_draft"] = self.store.get_draft(page.source_id, "note")
        return payload


def make_handler(application: PortalApplication) -> type[BaseHTTPRequestHandler]:
    class PortalHandler(BaseHTTPRequestHandler):
        server_version = "CantonResearchPortal/0.1"

        def log_message(self, format: str, *args: object) -> None:
            print(f"[portal] {self.address_string()} {format % args}")

        def _origin(self) -> str | None:
            origin = self.headers.get("Origin")
            return origin if write_origin_allowed(origin) else None

        def _require_write_origin(self) -> None:
            origin = self.headers.get("Origin")
            if not write_origin_allowed(origin):
                raise PermissionError("Write requests are limited to the local portal")

        def _send(self, status: int, payload: object) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            origin = self._origin()
            if origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> dict:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2 * 1024 * 1024:
                raise ValueError("Request body is too large")
            raw = self.rfile.read(length) if length else b"{}"
            value = json.loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise ValueError("JSON body must be an object")
            return value

        def _route(self) -> tuple[str, list[str], dict[str, list[str]]]:
            parsed = urlparse(self.path)
            parts = [part for part in parsed.path.split("/") if part]
            return parsed.path, parts, parse_qs(parsed.query)

        def _guard(self, action: Callable[[], None]) -> None:
            try:
                action()
            except KeyError as error:
                self._send(HTTPStatus.NOT_FOUND, {"error": str(error)})
            except (ValueError, json.JSONDecodeError) as error:
                self._send(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            except (ContentConflictError, DraftConflictError) as error:
                self._send(HTTPStatus.CONFLICT, {"error": str(error)})
            except PermissionError as error:
                self._send(HTTPStatus.FORBIDDEN, {"error": str(error)})
            except Exception as error:
                self._send(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": f"Unexpected portal error: {error}"},
                )

        def do_OPTIONS(self) -> None:
            self.send_response(HTTPStatus.NO_CONTENT)
            origin = self._origin()
            if origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_GET(self) -> None:
            self._guard(self._get)

        def _get(self) -> None:
            path, parts, query = self._route()
            if path == "/health":
                self._send(HTTPStatus.OK, {"status": "ok"})
                return
            if path == "/api/config":
                self._send(
                    HTTPStatus.OK,
                    {
                        "upstream_commit": application.content.upstream_commit,
                        "documents": len(application.content.pages),
                        "indexed_documents": application.indexed_documents,
                        "scope_profile": application.content.scope_profile_summary(),
                        "settings": application.store.settings(),
                    },
                )
                return
            if path == "/api/page":
                value = query.get("path", [""])[0]
                self._send(HTTPStatus.OK, application.page_payload(value))
                return
            if path == "/api/compare":
                value = query.get("path", [""])[0]
                page = application.content.page(value)
                self._send(HTTPStatus.OK, application.content.comparison(page))
                return
            if path == "/api/pages/status":
                rows = application.content.status_rows(
                    application.store.all_progress(), application.store.all_favorites()
                )
                self._send(HTTPStatus.OK, {"items": rows})
                return
            if path == "/api/claims":
                self._send(HTTPStatus.OK, {"items": application.content.claims()})
                return
            if path == "/api/questions":
                self._send(HTTPStatus.OK, {"items": application.content.questions()})
                return
            if path == "/api/changes":
                self._send(HTTPStatus.OK, {"items": application.content.changes()})
                return
            if path == "/api/scope":
                rows = application.content.status_rows(
                    application.store.all_progress(), application.store.all_favorites()
                )
                self._send(
                    HTTPStatus.OK,
                    {
                        "profile": application.content.scope_profile_summary(),
                        "items": [row for row in rows if row["scope"] == "excluded"],
                    },
                )
                return
            if path == "/api/search":
                value = query.get("q", [""])[0]
                limit = int(query.get("limit", ["30"])[0])
                self._send(
                    HTTPStatus.OK,
                    {"query": value, "items": application.store.search(value, limit)},
                )
                return
            if len(parts) == 4 and parts[:2] == ["api", "drafts"]:
                draft = application.store.get_draft(parts[2], parts[3])
                self._send(HTTPStatus.OK, {"draft": draft})
                return
            self._send(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})

        def do_PUT(self) -> None:
            self._guard(self._put)

        def _put(self) -> None:
            self._require_write_origin()
            _, parts, _ = self._route()
            body = self._read_json()
            if len(parts) == 3 and parts[:2] == ["api", "progress"]:
                page = application.content.page(parts[2])
                status = application.store.set_progress(page.source_id, str(body.get("status")))
                self._send(HTTPStatus.OK, {"source_id": page.source_id, "status": status})
                return
            if len(parts) == 3 and parts[:2] == ["api", "favorites"]:
                page = application.content.page(parts[2])
                favorite = body.get("favorite")
                if not isinstance(favorite, bool):
                    raise ValueError("Favorite must be a boolean")
                if favorite and application.content.research(page)["scope"] == "excluded":
                    raise ValueError("An excluded page must be included before favoriting")
                favorite = application.store.set_favorite(page.source_id, favorite)
                self._send(
                    HTTPStatus.OK,
                    {"source_id": page.source_id, "favorite": favorite},
                )
                return
            if len(parts) == 4 and parts[:2] == ["api", "drafts"]:
                page = application.content.page(parts[2])
                draft = application.store.save_draft(
                    page.source_id,
                    parts[3],
                    str(body.get("content", "")),
                    body.get("base_file_sha256"),
                    body.get("expected_version"),
                )
                self._send(HTTPStatus.OK, draft)
                return
            if len(parts) == 4 and parts[:2] == ["api", "pages"] and parts[3] == "scope":
                page = application.content.page(parts[2])
                research = application.content.publish_scope(
                    page,
                    str(body.get("scope", "")),
                    str(body.get("reason", "")),
                    body.get("base_file_sha256"),
                )
                if research["scope"] == "excluded":
                    application.store.set_favorite(page.source_id, False)
                self._send(HTTPStatus.OK, research)
                return
            self._send(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})

        def do_POST(self) -> None:
            self._guard(self._post)

        def _post(self) -> None:
            self._require_write_origin()
            _, parts, _ = self._route()
            body = self._read_json()
            if len(parts) == 4 and parts[:2] == ["api", "pages"] and parts[3] == "summary":
                page = application.content.page(parts[2])
                lines = body.get("lines", [])
                if not isinstance(lines, list):
                    raise ValueError("Summary lines must be a list")
                research = application.content.publish_summary(
                    page,
                    [str(line) for line in lines],
                    body.get("base_file_sha256"),
                    str(body.get("status", "human_edited")),
                )
                self._send(HTTPStatus.OK, research)
                return
            if self.path == "/api/search/rebuild":
                count = application.store.rebuild_search(
                    application.content.search_documents()
                )
                application.indexed_documents = count
                self._send(HTTPStatus.OK, {"indexed_documents": count})
                return
            self._send(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})

    return PortalHandler


def serve(host: str = "127.0.0.1", port: int = 8787, rebuild_index: bool = True) -> None:
    application = PortalApplication(rebuild_index=rebuild_index)
    server = ThreadingHTTPServer((host, port), make_handler(application))
    print(
        f"Research API listening on http://{host}:{port} "
        f"with {application.indexed_documents} indexed documents"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
