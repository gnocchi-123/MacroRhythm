# MacroRhythm

MacroLens의 거시경제 수집·계산·이력을 재사용하는 미국 거시경제 대시보드 프로젝트입니다.
MacroRhythm은 웹 표시·시각화·주간 보고서·설명·알림을 담당합니다. 두 저장소는 독립적으로 관리합니다.

**현재 단계: R0 — Python 패키지 기반 및 연동·운영 설계.**
웹사이트, 데이터 수집기, MacroLens 어댑터, 보고서 생성기, 스케줄러, 이메일 발송기는 아직 없습니다.
R1~R6 기능, 실제 FRED/KIS 호출, 배포는 이번 범위에 포함하지 않았습니다.

## 확정 요구사항

- 초기 지표: `INDPRO`, `UNRATE`, `CPIAUCSL`, `DGS10`.
- 주간 보고서 발행 목표: 월요일 오전 9시, `Asia/Seoul`.
- 초기 접근: 개인 및 승인된 사용자만. JSON·보고서 등 원본 산출물도 보호합니다.
- PC·스마트폰 모두 지원하며 원자료·변환값·출처·전주 비교·과거 보고서를 제공합니다(후속 구현).
- v1은 R0~R5: 실제 자료 자동 갱신·정기 발행까지. 섹터 점수는 제외하며 R6는 M4 검증 후 선택 확장입니다.
- 월 추가 운영비 상한 목표: 10,000원 이내, 도메인·메일 등 실제 비용 합산. 서비스·요금제 선택은 미확정입니다.
- MacroLens 계수·계산 규칙과 M4 연구 코드는 변경하지 않습니다.

## 개발 시작

Python 3.12와 [uv](https://docs.astral.sh/uv/)가 필요합니다. `.python-version`은 3.12 계열을 선택하고,
`pyproject.toml`은 Python 3.12~3.14를 허용합니다. 이번 검증은 Python 3.12.14 / uv 0.13.5로 했습니다.
잠금 파일 `uv.lock`을 커밋해 개발 의존성을 재현합니다. 런타임 외부 의존성은 없습니다.

```bash
cd /workspace/MacroRhythm
# 현재 클라우드의 기본 캐시 경로는 읽기 전용이므로 쓰기 가능한 경로 사용
export UV_CACHE_DIR=/tmp/macrorhythm-uv-cache
export UV_LINK_MODE=copy
uv sync --locked
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
uv run --locked python -c 'import macrorhythm; print(macrorhythm.__version__)'
```

일반 로컬 환경에서는 저장소 루트로 이동하고 캐시 경로 설정을 생략해도 됩니다.
격리된 클라우드 작업에서는 기존 체크아웃을 사용하며 별도의 Git worktree를 만들 필요가 없습니다.
실행할 서버나 별도 서비스는 없습니다. R0 명령에는 API 키·개인정보·`.env`가 필요하지 않습니다.
`.env` 자동 로딩도 구현하지 않았으므로 사용하지 않는 `.env.example`은 만들지 않았습니다.

## 파일 안내

| 경로 | 역할 |
| --- | --- |
| `pyproject.toml`, `uv.lock`, `.python-version` | 패키징·개발 도구·Python 버전 선택 |
| `src/macrorhythm/` | 버전만 제공하는 R0 패키지 기반 |
| `tests/` | 설치된 패키지 및 연동 계약의 양성·음성 테스트 |
| [docs/development_plan_v0.1.md](docs/development_plan_v0.1.md) | 확정 요구사항·기술 제안·단계 및 진입 조건 |
| [docs/r0_plan_review.md](docs/r0_plan_review.md) | 첨부 원문과 구현/설계의 대조·정정 기록 |
| [docs/macrolens_integration.md](docs/macrolens_integration.md) | 확인한 MacroLens 구조 및 제안 계약 |
| [docs/architecture_operations.md](docs/architecture_operations.md) | 정적 사이트·접근 제한·발행·비용 설계 |
| [docs/r0_validation.md](docs/r0_validation.md) | 검증 결과와 미확정 사항 |
| [docs/README.md](docs/README.md) | 문서 탐색 및 상태 구분 |

JSON Schema와 합성 예제는 `docs/contracts/`에 있습니다. **제안된 계약**이며 실제 exporter나
소비자가 아닙니다. 내부 예제의 섹터 점수는 원본 보존·검증용이며 v1 제품 표시에서 제외합니다.
예제 수치·점수는 실제 경제 자료나 투자 추천이 아닙니다.

## 보안과 변경 범위

키·이메일 주소·사용자 명단·실데이터는 Git에 넣지 않습니다. `.gitignore`는 `.env*`, 로컬 키,
`data/`, `reports/`, `artifacts/`, `site/`, `local/`을 제외합니다. 이 규칙은 이미 추적된 파일의
유출을 막아주지 않으므로 변경사항도 직접 검토해야 합니다.
MacroLens는 런타임 의존성으로 설치하거나 소스를 복제하지 않았습니다. 연동은 독립 산출물 경계를
통하도록 설계했습니다. R0 변경은 초기 로컬 `R0`에서 작업했고 최종 검수용 `docs/r0-plan` 브랜치로 보존했습니다.
사용자의 최종 검수 요청에 따라 커밋·push·main 대상 PR을 준비하며, main 병합과 배포는 수행하지 않습니다.
