# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

반도체 회사 **S-Semi**의 **반도체 시료 생산주문관리 시스템** 개발을 위한 4개 PoC 중 **PoC 4: Dummy 데이터 생성 Tool**이다.
시스템은 시료의 주문, 재고, 공정 현황을 관리하며 콘솔 기반으로 동작한다.

### 4개 PoC 전체 구성

| # | 이름 | 역할 |
|---|------|------|
| 1 | MVC 스켈레톤 | Model / Controller / View 패키지 구조와 역할 분리 |
| 2 | 데이터 영속성 | JSON 기반 저장·불러오기, CRUD |
| 3 | 데이터 모니터링 Tool | 콘솔 실시간 데이터 상태 조회 관리자 도구 |
| **4** | **Dummy 데이터 생성 Tool** | **테스트용 더미 데이터를 생성하여 DB(PoC 2 기반)에 저장** |

> **현재 이 레포지토리는 PoC 4만 개발한다.** PoC 4 범위 외의 기능은 추가하지 않는다.

## 개발 원칙

- **PoC 간 독립성 필수**: 각 PoC는 서로를 직접 import하지 않는다. 다른 PoC의 기능이 필요한 경우 `Protocol` 또는 추상 인터페이스(ABC)를 정의하고 이 PoC 내에서 구현체를 제공한다.
- **모듈화**: `dummy_generator/` 패키지를 독립적으로 설치·import 가능하도록 구성하여, 추후 통합 시스템에서 `from dummy_generator import ...` 형태로 사용할 수 있게 한다.

## 디렉터리 구조

```
DummyDataGenerator-BaeSungSu-24066680/
├── dummy_generator/          # 핵심 패키지 (외부 import 대상)
│   ├── __init__.py
│   ├── main.py               # 콘솔 진입점
│   ├── generators/           # 도메인별 더미 데이터 생성기
│   │   ├── __init__.py
│   │   ├── base.py           # 추상 Generator 인터페이스
│   │   ├── customer.py       # 고객 더미 데이터
│   │   ├── order.py          # 주문 더미 데이터
│   │   ├── inventory.py      # 재고 더미 데이터
│   │   └── process.py        # 공정 현황 더미 데이터
│   ├── db/                   # DB 연동 인터페이스 (PoC 2 독립성 유지)
│   │   ├── __init__.py
│   │   ├── interface.py      # DBRepository Protocol 정의
│   │   └── json_db.py        # JSON 파일 기반 구현체
│   └── models/               # 데이터 스키마 (dataclass / TypedDict)
│       ├── __init__.py
│       └── schemas.py
├── data/                     # 생성된 JSON 더미 데이터 저장 위치
├── .venv/                    # Python 가상환경 (Python 3.14.3)
├── .gitignore
└── CLAUDE.md
```

## 실행 명령

```bash
# 가상환경 활성화 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 더미 데이터 생성 Tool 실행
python -m dummy_generator.main

# 단일 모듈 테스트
python -m dummy_generator.generators.order

# 테스트 실행 (pytest 사용 시)
python -m pytest
```

## 아키텍처 핵심

### DB 인터페이스 분리
`db/interface.py`에 `DBRepository` Protocol을 정의한다. 실제 PoC 2 코드를 import하지 않고, 동일한 시그니처를 가진 `json_db.py` 구현체를 제공하여 PoC 간 독립성을 보장한다.

```python
# db/interface.py 예시
from typing import Protocol, Any

class DBRepository(Protocol):
    def save(self, collection: str, data: dict) -> None: ...
    def find_all(self, collection: str) -> list[dict]: ...
    def clear(self, collection: str) -> None: ...
```

### 더미 데이터 도메인
S-Semi 시스템의 주요 엔티티:
- **Customer**: 고객사 정보
- **SampleOrder**: 반도체 시료 주문 (품목, 수량, 납기일, 상태)
- **Inventory**: 재고 현황 (시료 종류, 수량, 위치)
- **ProcessStatus**: 공정 단계별 현황 (설계, 제조, 검사, 출하)
