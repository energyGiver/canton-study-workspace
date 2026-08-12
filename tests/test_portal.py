from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from portal.build import _localized_navigation, _translated_navigation_entries
from portal.content import (
    ContentRepository,
    canonical_path,
    extract_summary,
    parse_frontmatter,
    render_frontmatter,
    replace_section,
)
from portal.store import DraftConflictError, PortalStore
from portal.server import write_origin_allowed
from portal.validate import _frontmatter_syntax_errors, validate_workspace


ROOT = Path(__file__).resolve().parents[1]


class ContentHelpersTest(unittest.TestCase):
    def test_korean_navigation_preserves_nested_groups(self) -> None:
        entries = [
            "overview/one",
            {
                "group": "Nested",
                "pages": ["overview/two", "overview/three"],
            },
        ]
        translated = _translated_navigation_entries(
            entries, {"overview/one", "overview/three"}
        )
        self.assertEqual(
            translated,
            [
                "ko/overview/one",
                {"group": "Nested", "pages": ["ko/overview/three"]},
            ],
        )

    def test_korean_navigation_deduplicates_official_routes(self) -> None:
        seen: set[str] = set()
        first = _translated_navigation_entries(
            ["overview/one"], {"overview/one"}, seen
        )
        second = _translated_navigation_entries(
            ["overview/one"], {"overview/one"}, seen
        )
        self.assertEqual(first, ["ko/overview/one"])
        self.assertEqual(second, [])

    def test_localized_navigation_partitions_english_and_korean(self) -> None:
        products = [{"product": "Overview", "groups": []}]
        korean_groups = [{"group": "Overview", "pages": ["ko/overview/one"]}]
        navigation = _localized_navigation(products, korean_groups)
        self.assertNotIn("products", navigation)
        self.assertEqual(
            navigation["languages"],
            [
                {
                    "language": "en",
                    "default": True,
                    "products": products,
                },
                {
                    "language": "ko",
                    "products": [
                        {
                            "product": "한글 번역",
                            "icon": "language",
                            "groups": korean_groups,
                        }
                    ],
                },
            ],
        )

    def test_canonical_path_normalizes_locales_and_suffixes(self) -> None:
        self.assertEqual(
            canonical_path("/ko/overview/understand/what-is-canton.mdx?x=1"),
            "overview/understand/what-is-canton",
        )

    def test_frontmatter_and_summary_round_trip(self) -> None:
        metadata = {"source_id": "SRC-TEST", "scope": "included"}
        body = replace_section("", "Three-line summary", "1. One\n2. Two\n3. Three")
        rendered = render_frontmatter(metadata) + body
        parsed_metadata, parsed_body = parse_frontmatter(rendered)
        self.assertEqual(parsed_metadata["source_id"], "SRC-TEST")
        self.assertEqual(extract_summary(parsed_body), ["One", "Two", "Three"])

    def test_repository_resolves_manifest_page(self) -> None:
        repository = ContentRepository()
        page = repository.page("overview/understand/what-is-canton")
        self.assertEqual(page.source_id, "SRC-5129D11A60")
        self.assertFalse(repository.research(page)["stale"])
        self.assertEqual(len(repository.research(page)["summary"]), 3)
        self.assertIn("CLM-001", repository.research(page)["related_claim_ids"])
        self.assertIn("OQ-001", repository.research(page)["related_question_ids"])
        self.assertTrue(repository.translation(page)["available"])
        self.assertFalse(repository.translation(page)["stale"])
        comparison = repository.comparison(page)
        self.assertIn("Canton Network is a public layer 1", comparison["english"])
        self.assertIn("Canton Network는 privacy-preserving", comparison["korean"])
        self.assertTrue(repository.claims()[0]["sources"])
        self.assertGreater(len(repository.claims()), 0)
        self.assertGreater(len(repository.questions()), 0)

    def test_repository_falls_back_to_published_snapshot(self) -> None:
        repository = ContentRepository()
        page = repository.page(
            "global-synchronizer/extension-synchronizers/private-synchronizers"
        )
        self.assertFalse(repository.upstream_path(page).exists())
        self.assertTrue(repository.official_source_path(page).exists())
        self.assertEqual(repository.source_sha256(page), page.published_sha256)

    def test_public_testnet_scope_profile_is_conservative_and_stable(self) -> None:
        repository = ContentRepository()
        excluded = [
            row for row in repository.status_rows({}) if row["scope"] == "excluded"
        ]
        self.assertEqual(len(excluded), 153)
        self.assertEqual(
            repository.research(repository.page("appdev/app-rewards"))["scope"],
            "excluded",
        )
        self.assertEqual(
            repository.research(
                repository.page(
                    "global-synchronizer/extension-synchronizers/private-synchronizers"
                )
            )["scope"],
            "included",
        )
        self.assertEqual(
            repository.research(repository.page("overview/reference/topology"))["scope"],
            "included",
        )
        self.assertEqual(
            repository.research(
                repository.page("integrations/wallet-gateway/overview")
            )["scope"],
            "included",
        )

    def test_page_scope_override_wins_over_public_testnet_profile(self) -> None:
        repository = ContentRepository()
        research = repository.research(
            repository.page("overview/understand/what-is-canton")
        )
        self.assertEqual(research["scope"], "included")
        self.assertEqual(research["scope_source"], "page-override")


class StoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.store = PortalStore(
            Path(self.temporary.name) / "research.sqlite", ROOT / "portal" / "migrations"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_progress_defaults_and_updates(self) -> None:
        self.assertEqual(self.store.get_progress("SRC-TEST"), "unreviewed")
        self.store.set_progress("SRC-TEST", "in_progress")
        self.assertEqual(self.store.get_progress("SRC-TEST"), "in_progress")

    def test_draft_uses_optimistic_version(self) -> None:
        first = self.store.save_draft("SRC-TEST", "summary", "draft", None, 0)
        self.assertEqual(first["version"], 1)
        with self.assertRaises(DraftConflictError):
            self.store.save_draft("SRC-TEST", "summary", "stale", None, 0)

    def test_full_text_search(self) -> None:
        count = self.store.rebuild_search(
            [
                {
                    "source_id": "SRC-TEST",
                    "path": "/test",
                    "language": "en",
                    "kind": "official",
                    "title": "Synchronizer architecture",
                    "content": "Sequencers order encrypted envelopes.",
                }
            ]
        )
        self.assertEqual(count, 1)
        results = self.store.search("sequencer")
        self.assertEqual(results[0]["source_id"], "SRC-TEST")


class WorkspaceValidationTest(unittest.TestCase):
    def test_invalid_double_quoted_frontmatter_is_rejected(self) -> None:
        text = '---\ntitle: "Example"\ndescription: "new ContractId("test")"\n---\n'
        self.assertEqual(
            _frontmatter_syntax_errors(text),
            ["line 3 has an invalid double-quoted value"],
        )

    def test_shared_research_metadata_is_valid(self) -> None:
        report = validate_workspace()
        self.assertTrue(report.valid, report.errors)
        self.assertGreaterEqual(report.summaries, 1)
        self.assertGreaterEqual(report.translations, 1)

    def test_write_origin_is_limited_to_local_portal(self) -> None:
        self.assertTrue(write_origin_allowed(None))
        self.assertTrue(write_origin_allowed("http://localhost:3000"))
        self.assertTrue(write_origin_allowed("http://127.0.0.1:4100"))
        self.assertFalse(write_origin_allowed("https://localhost:3000"))
        self.assertFalse(write_origin_allowed("https://example.com"))


if __name__ == "__main__":
    unittest.main()
