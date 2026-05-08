from dummy_generator.db.json_db import JsonDB
from dummy_generator.generators.customer import CustomerGenerator
from dummy_generator.generators.inventory import InventoryGenerator
from dummy_generator.generators.order import OrderGenerator
from dummy_generator.generators.process import ProcessGenerator

_MENU = """
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
==========================================="""

_COLLECTIONS = ("customers", "orders", "inventory", "process_status")


def _read_int(prompt: str, min_val: int = 1) -> int:
    while True:
        try:
            val = int(input(prompt))
            if val >= min_val:
                return val
            print(f"  {min_val} 이상의 숫자를 입력하세요.")
        except ValueError:
            print("  숫자를 입력하세요.")


def _show_counts(db: JsonDB) -> None:
    for col in _COLLECTIONS:
        print(f"  {col}: {db.count(col)}건")


def run(data_dir: str = "data") -> None:
    db = JsonDB(data_dir=data_dir)

    while True:
        print(_MENU)
        _show_counts(db)
        print()
        choice = input("선택 > ").strip()

        if choice == "1":
            n = _read_int("생성할 고객 수: ")
            CustomerGenerator(db).generate(n)
            print(f"  ✓ 고객 {n}건 생성 완료")

        elif choice == "2":
            ids = [c["id"] for c in db.find_all("customers")]
            if not ids:
                print("  ! 고객 데이터가 없습니다. 먼저 고객(1번)을 생성하세요.")
                continue
            n = _read_int("생성할 주문 수: ")
            OrderGenerator(db, ids).generate(n)
            print(f"  ✓ 주문 {n}건 생성 완료")

        elif choice == "3":
            n = _read_int("생성할 재고 항목 수: ")
            InventoryGenerator(db).generate(n)
            print(f"  ✓ 재고 {n}건 생성 완료")

        elif choice == "4":
            ids = [o["id"] for o in db.find_all("orders")]
            if not ids:
                print("  ! 주문 데이터가 없습니다. 먼저 주문(2번)을 생성하세요.")
                continue
            n = _read_int("생성할 공정 현황 수: ")
            ProcessGenerator(db, ids).generate(n)
            print(f"  ✓ 공정 현황 {n}건 생성 완료")

        elif choice == "5":
            n = _read_int("기준 건수 (고객 n명 → 주문 n×4, 재고 n×2, 공정 n×4): ")
            customers = CustomerGenerator(db).generate(n)
            cids = [c["id"] for c in customers]
            orders = OrderGenerator(db, cids).generate(n * 4)
            InventoryGenerator(db).generate(n * 2)
            ProcessGenerator(db, [o["id"] for o in orders]).generate(n * 4)
            print(f"  ✓ 세트 생성 완료 — 고객 {n}, 주문 {n*4}, 재고 {n*2}, 공정 {n*4}")

        elif choice == "6":
            print(f"  컬렉션 목록: {', '.join(_COLLECTIONS)}")
            coll = input("  초기화할 컬렉션 이름: ").strip()
            if coll not in _COLLECTIONS:
                print(f"  ! 알 수 없는 컬렉션: {coll}")
                continue
            db.clear(coll)
            print(f"  ✓ {coll} 초기화 완료")

        elif choice == "0":
            print("  종료합니다.")
            break

        else:
            print("  올바른 메뉴 번호를 선택하세요.")


if __name__ == "__main__":
    run()
