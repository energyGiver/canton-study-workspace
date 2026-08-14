# Canton Documentation Research Workspace

## 이 프로젝트는 무엇인가

이 프로젝트는 **공식 Canton 문서를 그대로 보존한 로컬 문서 사이트에 번역, 검토 상태, Favorite, 3줄 요약, Claim/Open Question을 결합한 팀 연구 Workspace**입니다.

원본은 `upstream/cf-docs/`에서 읽기 전용으로 유지하고, 번역과 공동 연구 결과는 Git으로 공유하며, 개인의 Favorite와 검토 상태는 로컬 SQLite에만 저장합니다. Canton source code 분석, Node 실행 및 runtime 검증은 현재 범위에 포함하지 않습니다.

## 나만의 Canton Docs 실행

필수 조건은 Git, Python 3, Node.js/npm과 `npx`입니다. 최초 실행 시 공식 문서 submodule을 받은 후 portal을 시작합니다.

```bash
git submodule update --init --recursive
python3 -m portal dev
```

실행이 완료되면 다음 주소를 사용합니다.

- 문서 UI: `http://localhost:3000`
- 로컬 Research API: `http://127.0.0.1:8787`

종료하려면 실행한 terminal에서 `Ctrl-C`를 누릅니다. Port를 바꾸려면 다음과 같이 실행합니다.

```bash
python3 -m portal dev --api-port 8788 --docs-port 3001
```

개별 단계만 실행할 수도 있습니다.

```bash
python3 -m portal build       # ignored local site만 다시 합성
python3 -m portal refresh     # 실행 중인 preview를 끄지 않고 번역/navigation 갱신
python3 -m portal serve       # Research API와 search index만 실행
python3 -m portal index       # local search index만 재생성
python3 -m portal validate    # shared artifact를 변경하지 않고 검증
python3 -m portal translations # 번역/로컬 제외/backlog 수와 todo JSON 생성
```

`portal refresh`는 소수의 번역을 작업 중인 preview에 반영할 때 사용합니다. 처음으로 수백 page를 추가하거나 official navigation 전체가 바뀐 경우에는 대규모 hot compile을 피하기 위해 작업을 마친 뒤 `portal dev`를 한 번 재시작하는 편이 안전합니다.

## 공식 Canton 문서에 Workspace가 별도로 추가한 기능

| 기능 | 사용 방법 | 저장 위치 |
| --- | --- | --- |
| 다국어 문서 | 상단 language selector에서 ENG/KOR 선택, 번역이 없는 page는 English 사용 | Git의 `translations/<language>/` |
| Favorite | sidebar 제목 왼쪽 `☆`를 누르면 `★`, 다시 누르면 `☆` | 개인 SQLite |
| Favorites 모아보기 | 우측 상단 `★ Favorites`에서 제품 구분 없이 Favorite page만 조회 | 개인 SQLite를 실시간 조회 |
| 검토/scope 상태 | sidebar 제목 오른쪽의 한 box를 순환 | 아래 상태 설명 참조 |
| 3줄 요약 | 본문 제목 아래 접힌 `Research summary`를 열어 조회 및 수정 | Draft는 SQLite, Publish하면 Git Markdown |
| ENG/KOR 비교 | 번역 page의 `Compare ENG/KOR`로 원문과 번역을 나란히 비교 | 읽기 전용 조합 |
| Evidence capture | 원문을 선택해 Claim 또는 Open Question 초안을 생성 | Draft는 SQLite, 확정본은 Git Markdown |
| Inline comment | 문장이나 한 단락을 선택한 뒤 `💬 Comment`로 source-anchored comment 작성 | 작성 중 draft는 SQLite, Publish하면 Git Markdown |
| Comments 모아보기 | 우측 상단 `💬 Comments`에서 제품 구분 없이 comment가 있는 page와 comment를 통합 조회 | Git의 `research/comments/`를 실시간 조회 |
| Local comment UX | 공식 문서의 하단 Giscus 대신 source-anchored workspace comment만 사용 | Giscus는 generated local site에서만 비활성화 |
| 통합 검색 | English, 번역 및 공개 research note를 한 번에 검색 | 재생성 가능한 SQLite FTS5 index |
| Research dashboard | Progress, excluded page, upstream change, Claim/Open Question을 별도 화면에서 조회 | SQLite와 Git artifact를 조합 |
| 원문 변경 감지 | upstream SHA와 summary/translation의 `source_sha256`를 비교해 stale 표시 | Git metadata |
| Image/Mermaid 보존 | 원본 image를 재사용하고 Mermaid source를 English/KOR 양쪽에서 동일하게 render | 원본 asset과 generated preview |

### Favorite 토글

왼쪽 box는 Favorite만 담당하며 scope와 독립적입니다.

```text
☆ Not favorite → ★ Favorite → ☆ Not favorite
```

`★`는 dark theme에서 보라색 음영으로 표시됩니다. Scope 제외 page도 나중에 참고할 수 있도록 Favorite에 저장할 수 있습니다.

### 검토 및 scope 토글

오른쪽 box는 다음 순서로 동작합니다.

```text
빈 box, 검토 전 → 초록 ✓, 검토 완료 → 회색 ✕, scope 제외 → 빈 box, 검토 전
```

- 검토 전과 검토 완료는 개인 SQLite 상태입니다.
- 완료에서 scope 제외로 변경할 때는 제외 이유를 입력하며, 이 결정은 팀 공유 대상인 page research Markdown에 기록됩니다.
- Scope 제외에서 빈 box로 변경하면 명시적인 scope 포함 override가 기록되고 개인 검토 상태는 `unreviewed`로 돌아갑니다.
- 기존 `in_progress` 상태는 사용하지 않으며 발견되면 `unreviewed`로 migration합니다.

## 로컬 저장과 팀 공유의 경계

판단 기준은 간단합니다. **개인적이고 자주 바뀌거나 재생성 가능한 것은 SQLite, 다른 팀원이 검토하고 재사용해야 하는 것은 Git**에 저장합니다.

### 로컬 SQLite, 공유하지 않음

경로: `data/local/research.sqlite`

- Favorite
- 개인 page 검토 상태: `unreviewed`, `complete`
- Publish 전 3줄 요약 및 evidence autosave draft
- Publish 전 inline comment autosave draft
- UI setting과 향후 개인 bookmark/highlight
- Full-text search index와 parsed document cache
- 번역 제외 정책: `data/local/translation-exclusions.json`

`data/local/`과 `.generated/`는 Git에 commit하지 않으며 network drive에서 공동 사용하지 않습니다. 각 팀원이 자신의 DB를 가집니다.

번역 제외 정책도 이 원칙을 따릅니다. 현재 public testnet 연구에 가치가 낮은 generated API reference와 Global Synchronizer 전용 application page는 정확한 official path와 제외 이유를 로컬 JSON에 기록합니다. `portal translations`와 upstream sync는 그 exact path만 건너뛰므로, 새 official path는 자동으로 제외되지 않고 다시 검토 대상이 됩니다.

### Git, 팀 공유 및 review 대상

- 비공식 번역: `translations/<language>/`
- 공개 3줄 요약과 page별 분석: `research/pages/`
- 공개 inline comment: `research/comments/<source_id>/<comment_id>.md`
- 기본 scope profile과 page scope override: `research/scope/`, page research frontmatter
- Claim/Open Question: `claims/`, `questions/`
- Topic, map, glossary, use case: `topics/`, `maps/`, `glossary/`, `use-cases/`
- 공식 evidence snapshot과 manifest: `corpus/`
- 공식 문서 version pointer: `upstream/cf-docs/` submodule commit

## Inline comment 사용과 충돌 방지

공식 문서 본문에서 한 문장이나 한 단락을 선택하면 작은 `💬 Comment` action이 나타납니다. 작성 중인 내용은 local SQLite에 자동 저장되고, `Publish to Git`을 눌러야 팀 공유 Markdown이 생성됩니다. 공개된 문장은 보라색 highlight로 보이며 hover하면 comment를 읽거나 수정/삭제할 수 있습니다. 우측 상단 `💬 Comments`는 모든 제품의 공개 comment를 page별로 묶어 보여줍니다.

Comment는 공식 MDX에 삽입하지 않습니다. 각 comment는 선택한 exact quote, 앞뒤 문맥, text position, source ID, source commit과 SHA-256을 별도 파일에 저장합니다. Portal은 먼저 같은 위치를 확인하고, 실패하면 앞뒤 문맥까지 일치하는 quote가 정확히 하나일 때만 anchor를 복구합니다. 원문 변경 뒤 후보가 없거나 여러 개면 임의의 문장에 붙이지 않고 source-changed 상태로 남깁니다. 이 방식은 [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)의 `TextQuoteSelector`와 `TextPositionSelector` 원칙을 따르며, highlight는 원문 DOM을 감싸지 않는 [CSS Custom Highlight API](https://www.w3.org/TR/css-highlight-api-1/)를 사용합니다.

## 다른 언어 추가와 저장 용량

다른 언어도 같은 구조로 지원할 수 있습니다. 현재 composer는 `translations/ko/`만 자동 포함하므로, 예를 들어 일본어를 추가하려면 `translations/ja/<official-path>.mdx`와 함께 build navigation에 `ja`를 등록하는 작은 code 확장이 필요합니다. AI 초안을 사용할 수 있지만 기술 용어, code, link, MDX structure와 source hash를 보존하고 사람 review 전에는 `ai_draft`로 표시해야 합니다.

용량 증가는 감당 가능한 수준입니다. 현재 측정값은 다음과 같습니다.

- 공식 `cf-docs` submodule 전체: 약 72MB
- 한국어 번역 862개 MDX: 약 10MB, 최신 진행률은 [translation status](translations/STATUS.md) 참조
- 생성된 전체 preview: 약 79MB
- 공식 image asset: 약 32MB이며 모든 언어가 원본을 기본 재사용

따라서 현재 corpus 전체를 한 언어로 번역하면 Git tracked text가 대략 8MB에서 10MB 증가할 것으로 예상됩니다. 세 언어를 추가해도 text 증가는 대략 25MB에서 30MB 수준입니다. 다만 언어별 image를 별도로 제작하면 image 용량이 추가되므로, **공통 image와 Mermaid는 원본을 재사용하고 번역 MDX만 언어별로 저장**하는 방식을 권장합니다. `.generated/site/`는 매번 재생성되고 Git에 포함되지 않으므로 repository history를 키우지 않습니다.

## 검증 및 공식 문서 업데이트

Before publishing shared research, run:

```bash
python3 -m portal validate
python3 -m unittest discover -s tests -v
```

Check official `cf-docs` changes with `python3 -m portal sync`. Apply the latest `origin/main` commit with `python3 -m portal sync --update`, inspect the changed submodule pointer and stale-content dashboard, then commit the reviewed update separately. Run `python3 -m portal translations` after every update. It compares official file-backed navigation against complete translations and the Git-ignored local exclusion policy, then writes the remaining todo to `.generated/translation-backlog.json`.

## Research 목적과 읽는 순서

This repository is a documentation-only technical knowledge base for Canton Network. Official Canton documentation is the primary evidence source because this phase is intended to reconstruct the documented protocol and application mental model before any source-code analysis or runtime verification.

The knowledge base is useful only under three conditions: conclusions remain traceable to the corpus, inference is labeled, and unresolved documentation gaps remain open rather than being filled from model memory.

1. Read [the concept map](maps/concept-map.md) for the learning sequence and cross-topic dependencies.
2. Follow the topic sequence in [the topic index](topics/README.md).
3. Use [the claim ledger](claims/claim-ledger.md) for classified conclusions and [the open questions registry](questions/open-questions.md) for gaps.
4. Consult [the glossary](glossary/canton-glossary.md) when terminology differs across documentation areas.
5. Use `corpus/manifest.jsonl` to resolve a source ID to its exact URL, local file, headings, retrieval time, and checksum.
6. Use [the local research portal development design](development/local-research-portal.md) for the detailed storage and implementation design.

## Repository layout

| Path | Purpose |
| --- | --- |
| `corpus/` | Verbatim official Markdown snapshot, official index, checksums, and retrieval metadata |
| `maps/` | Learning map and lightweight Mermaid diagrams |
| `topics/` | Cross-document mechanism notes organized by technical topic |
| `claims/` | Important conclusions classified as `EXPLICIT`, `INFERRED`, or `UNCLEAR` |
| `questions/` | Documentation gaps and the later engineering-phase backlog |
| `research/comments/` | Git-tracked inline comments anchored to official or translated document text |
| `use-cases/` | Use cases derived from protocol and application mechanisms |
| `glossary/` | Curated terminology with ambiguity notes |
| `scripts/` | Reproducible official-document collector; it does not inspect Canton source code |
| `development/` | Development designs for the local documentation and research portal |
| `portal/` | Local site composer, research API, and browser overlay |
| `upstream/cf-docs/` | Pinned read-only official documentation submodule |

## Evidence model

- `EXPLICIT`: the cited official text directly states the conclusion.
- `INFERRED`: the conclusion follows from multiple cited facts; the reasoning is written out.
- `UNCLEAR`: the official corpus is incomplete, conflicting, or too imprecise to support one conclusion.

Topic notes use source IDs such as `SRC-A3F46FF397`. IDs are derived from source URLs and therefore remain stable if the official index is reordered. Local links support offline review; each note also lists the official URLs.

## Corpus snapshot

- Primary inventory: official `upstream/cf-docs/docs-main/docs.json` navigation
- Source commit: `5ce61f7ca8ec6ad9af3d5e19db3583588ba49d65`
- Retrieved: 2026-08-12
- Active official inventory: 1,160 file-backed MDX routes
- Korean translations: 862 complete pages
- Local translation exclusions: 298 exact paths
- Translation backlog: 0
- Historical discovery snapshot: 804 Markdown responses originally collected from `llms.txt`, retained under `corpus/docs/`
- Integrity: SHA-256 for every official MDX source file in the active manifest

See [corpus/README.md](corpus/README.md) for the manifest schema and refresh procedure.

## Phase boundary

This repository does not inspect Canton source repositories, execute tests, deploy LocalNet or nodes, run runtime experiments, or verify documentation against implementation. Documentation may describe those activities, but this phase records what the documentation says rather than performing them. Items requiring those methods are explicitly deferred in the open questions registry.

## Completion standard

This snapshot establishes the research structure, full official navigation inventory, dependency maps, topic mechanisms, classified claim ledger, curated glossary, use-case explanations, and an engineering backlog. Korean coverage is complete for every page not explicitly excluded by the local translation policy, but this is not a claim that all 1,160 pages have completed human research review. Future refreshes must diff the corpus first, then revisit translations and claims affected by changed sources.

## `preview ready`까지 시간이 걸리는 이유

`python3 -m portal dev`는 단순 web server 실행이 아니라 다음 작업을 순서대로 수행합니다.

1. 1,160개 공식 page와 모든 번역의 source ID, SHA-256, MDX 구조, code block 및 metadata를 검증합니다. 오류가 있으면 preview를 시작하지 않습니다.
2. 기존 `.generated/site/`를 지우고 pinned `upstream/cf-docs/docs-main/` 전체를 새로 복사합니다.
3. 번역 page, 필요한 image, Research page, ENG/KOR navigation, overlay JavaScript/CSS와 Mermaid fallback marker를 합성합니다.
4. Local Research API를 background thread로 시작하고 SQLite migration을 적용한 뒤 official English, 번역, 공개된 research note를 FTS5 full-text search index로 다시 만듭니다.
5. API indexing과 함께 `npx`가 고정된 Mintlify CLI를 준비하고 모든 MDX, route, navigation과 asset을 local preview로 compile합니다.

따라서 첫 실행, upstream/번역 page가 많을 때, Node package cache가 없을 때 시간이 더 걸립니다. 다음 로그는 오류가 아니라 각 단계의 완료 신호입니다.

```text
Research API listening on http://127.0.0.1:8787 with 1584 indexed documents
✓ preview ready
```

`1584 indexed documents`는 당시 실행 시점의 English 공식 page, 존재하는 번역 page와 공개된 research note를 합친 검색 row 수입니다. 번역이나 research note가 추가되면 숫자도 증가합니다. `preview ready`가 출력된 후에 `http://localhost:3000`을 여는 것이 안전합니다.
