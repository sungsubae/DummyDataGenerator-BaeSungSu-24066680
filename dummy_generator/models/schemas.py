from dataclasses import dataclass


@dataclass
class Customer:
    id: str
    name: str
    company: str
    contact: str
    email: str


@dataclass
class SampleOrder:
    id: str
    customer_id: str
    sample_type: str
    quantity: int
    due_date: str       # ISO 날짜 문자열 (YYYY-MM-DD)
    status: str         # 주문접수 / 생산중 / 검사중 / 출하완료


@dataclass
class Inventory:
    id: str
    sample_type: str
    quantity: int
    unit: str
    location: str


@dataclass
class ProcessStatus:
    id: str
    order_id: str
    stage: str          # 설계 / 제조 / 검사 / 출하
    status: str         # 대기 / 진행중 / 완료
    updated_at: str     # ISO 날짜시간 문자열
