# DummyDataGenerator — S-Semi PoC 4

반도체 시료 생산주문관리 시스템 개발을 위한 4개 PoC 중 **PoC 4: Dummy 데이터 생성 Tool**입니다.

## 실행

```powershell
.\.venv\Scripts\Activate.ps1
python -m dummy_generator.main
```

## 테스트

```powershell
python -m pytest
python -m pytest --cov=dummy_generator --cov-report=term-missing
```

## 구조

```
dummy_generator/
├── main.py           # 콘솔 진입점
├── models/schemas.py # 데이터 스키마 (Customer, SampleOrder, Inventory, ProcessStatus)
├── db/
│   ├── interface.py  # DBRepository Protocol
│   └── json_db.py    # JSON 파일 구현체
└── generators/       # 도메인별 더미 데이터 생성기
    ├── base.py
    ├── customer.py
    ├── order.py
    ├── inventory.py
    └── process.py
```

각 PoC는 `DBRepository Protocol`을 통해 서로 직접 의존하지 않습니다.
생성된 데이터는 `data/*.json`에 저장됩니다.
