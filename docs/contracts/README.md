# 교환 계약 제안과 합성 예제

- `macrolens-run-0.1.0.schema.json`: R0 제안, JSON Schema Draft 2020-12.
- `examples/sample-research-complete.json`: 원본 연구 모델 합성 실행, research_complete, 11개 섹터.
- `examples/sample-research-held.json`: 합성 입력에서 INDPRO를 메모리상 제외한 원본 실행, held, 점수 없음.
- `examples/sample-demo-complete.json`: 원본 기본 가상 모델 합성 실행, demo_complete, 가상 3개 섹터.

MacroLens main 커밋 `8f6bfa07ee74587e8ec4fc7e45cc9168895b14cc`의 원래 코드를
네트워크 차단(socket 연결 및 FRED urlopen 금지) 상태로 실행했습니다.
기준 시각은 `2026-10-05T09:00:00+09:00`이며, 실제 경제 관측이 아닙니다.
누락 실험은 입력 객체만 바꿨으며 소스·계수·계산 규칙은 수정하지 않았습니다.
각 실행은 `/tmp`의 별도 출력에 저장하고 MacroLens `load_run`으로 무결성을 확인했습니다.
예제의 `result`는 그 객체를 보존했고 envelope만 제안 형태로 감쌌습니다.
`exported_at`은 예제 작성 편의상 result.generated_at을 사용합니다. 실제 exporter는 미구현입니다.

`manifest_sha256`는 당시 생성된 manifest 원본 바이트 해시입니다. 전체 원본 bundle은 이 저장소에
포함하지 않았으므로 예제 파일만으로 manifest/입력 해시를 재검증할 수 없습니다.
테스트는 예제의 구조·상태 및 지원 범위를 검증하며, 전송/운영 무결성 검증 성공을 뜻하지 않습니다.
예제 run_id와 generated_at은 실행 당시 값이고 주간 발행/실제 수집 성공 기록이 아닙니다.
상태 검증 테스트는 외부 저장소·네트워크·API 키 없이 이 저장소만으로 다시 실행할 수 있습니다.

```bash
uv run --locked pytest -q tests/test_contract_examples.py
```

JSON Schema만으로 시점·해시·점수 합·원본 동일성을 모두 검증할 수 없습니다.
[연동 설계](../macrolens_integration.md)의 의미 검증은 R1에서 구현해야 합니다.

## 제품 표시 계약과 구분

첨부 개발계획의 `weekly_snapshot_v1`은 R1에서 별도로 구현할 네 지표 전용 표시 계약입니다.
이 폴더의 `macrolens.run` envelope는 내부 source 보존용이며 그 대체물이 아닙니다.
예제에 보존한 scores/순위/연구 메타데이터는 v1 웹·보고서·설명·이메일에 투영하지 않습니다.
섹터 점수는 M4 검증 이후 R6 별도 승인 범위입니다. 필드별 매핑·미구현 범위는
[연동 설계](../macrolens_integration.md)에 기록했습니다.
