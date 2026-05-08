# DummyDataGenerator — S-Semi PoC 4

반도체 회사 **S-Semi**의 *반도체 시료 생산주문관리 시스템* 개발을 위한 **PoC 4: Dummy 데이터 생성 Tool**입니다.

---

## 프로젝트 배경

S-Semi는 DRAM·NAND·Logic IC 등 다양한 반도체 시료를 여러 고객에게 납품합니다.
시스템 개발 전 검증을 위해 4개의 PoC를 순차적으로 진행하며, 이 레포지토리는 그 중 **4번째 단계**입니다.

| # | PoC | 역할 |
|---|-----|------|
| 1 | MVC 스켈레톤 | Model / Controller / View 패키지 구조 |
| 2 | 데이터 영속성 | JSON 기반 CRUD |
| 3 | 데이터 모니터링 Tool | 콘솔 실시간 조회 |
| **4** | **Dummy 데이터 생성 Tool** | **테스트용 더미 데이터 생성 및 DB 저장** |

> 각 PoC는 `Protocol`(인터페이스)을 통해 서로 독립적으로 구성되어, 추후 통합 시스템에서 `from dummy_generator import ...` 형태로 재사용할 수 있습니다.

---

## 디렉터리 구조

```
DummyDataGenerator-BaeSungSu-24066680/
├── dummy_generator/          # 핵심 패키지
│   ├── main.py               # 콘솔 진입점
│   ├── models/
│   │   └── schemas.py        # Customer / SampleOrder / Inventory / ProcessStatus
│   ├── db/
│   │   ├── interface.py      # DBRepository Protocol (PoC 2 독립성)
│   │   └── json_db.py        # JSON 파일 기반 구현체
│   └── generators/
│       ├── base.py           # BaseGenerator (ABC)
│       ├── customer.py       # 고객 더미 데이터
│       ├── order.py          # 주문 더미 데이터
│       ├── inventory.py      # 재고 더미 데이터
│       └── process.py        # 공정 현황 더미 데이터
├── tests/                    # pytest 테스트 (30개)
├── data/                     # 생성된 JSON 파일 저장 위치 (런타임 생성)
├── pyproject.toml            # pytest / coverage 설정
└── CLAUDE.md                 # Claude Code 가이드
```

---

## 실행 방법

### 1. 가상환경 활성화

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 2. Dummy 데이터 생성 Tool 실행

```powershell
python -m dummy_generator.main
```

실행하면 현재 DB 건수를 확인한 뒤 메뉴를 선택합니다.

```
===========================================
  S-Semi 더미 데이터 생성 Tool  (PoC 4)
===========================================
 1. 고객 데이터 생성
 2. 주문 데이터 생성        (고객 필요)
 3. 재고 데이터 생성
 4. 공정 현황 데이터 생성   (주문 필요)
 5. 전체 세트 일괄 생성
 6. 특정 컬렉션 초기화
 0. 종료
===========================================
  customers: 0건  orders: 0건  inventory: 0건  process_status: 0건
```

### 3. 테스트 실행

```powershell
# 전체 테스트
python -m pytest

# 커버리지 포함
python -m pytest --cov=dummy_generator --cov-report=term-missing

# 특정 파일만
python -m pytest tests/test_db.py -v
```

---

## 작동 원리

### 데이터 흐름

```
콘솔 메뉴 (main.py)
  └─ Generator 호출 (n건 생성 요청)
       └─ _make_one() × n  →  랜덤 데이터 생성
            └─ db.save()   →  data/*.json 에 누적 저장
```

### 연관 데이터 생성 (5번: 전체 세트)

주문은 고객 ID를, 공정 현황은 주문 ID를 참조합니다.
먼저 생성된 데이터의 ID를 DB에서 읽어 다음 Generator에 주입하여 **참조 무결성**을 유지합니다.

```
고객 n명 생성
  → customer_ids 추출 → 주문 n×4건 생성
      → order_ids 추출 → 공정 현황 n×4건 생성
재고 n×2건 생성 (독립)
```

### PoC 간 독립성 (DBRepository Protocol)

```python
# db/interface.py
class DBRepository(Protocol):
    def save(self, collection: str, record: dict) -> None: ...
    def find_all(self, collection: str) -> list[dict]: ...
    def find_by_id(self, collection: str, record_id: str) -> dict | None: ...
    def clear(self, collection: str) -> None: ...
    def count(self, collection: str) -> int: ...
```

PoC 2의 코드를 직접 import하지 않고 Protocol만 정의하여, 통합 시스템에서는 PoC 2의 구현체를 주입하면 됩니다.

### 생성 데이터 도메인

| 컬렉션 | 파일 | 주요 필드 |
|--------|------|-----------|
| customers | `data/customers.json` | name, company, contact, email |
| orders | `data/orders.json` | customer_id, sample_type, quantity, due_date, status |
| inventory | `data/inventory.json` | sample_type, quantity, unit, location |
| process_status | `data/process_status.json` | order_id, stage, status, updated_at |

**시료 종류**: DRAM-DDR5, NAND-Flash-3D, Logic-IC-7nm, SiC-MOSFET 등 12종  
**공정 단계**: 설계 → 제조 → 검사 → 출하  
**주문 상태**: 주문접수 / 생산중 / 검사중 / 출하완료

---

## 테스트 현황

```
30 passed in 0.82s

Name                                      Stmts   Miss  Cover
--------------------------------------------------------------
dummy_generator/db/json_db.py                29      0   100%
dummy_generator/generators/base.py           12      0   100%
dummy_generator/generators/customer.py       16      0   100%
dummy_generator/generators/inventory.py      11      0   100%
dummy_generator/generators/order.py          17      0   100%
dummy_generator/generators/process.py        17      0   100%
dummy_generator/models/schemas.py             9      0   100%
dummy_generator/main.py                      72     72     0%  ← 대화형 UI
--------------------------------------------------------------
TOTAL                                       186     72    61%
```

`main.py`는 대화형 콘솔 입력이 필요한 UI 코드로 자동 테스트 대상에서 제외됩니다.
