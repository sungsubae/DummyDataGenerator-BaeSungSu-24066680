import random
import uuid

from dummy_generator.generators.base import BaseGenerator
from dummy_generator.models.schemas import Customer

_SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"]
_GIVEN_NAMES = ["민준", "서준", "도윤", "주원", "하준", "지호", "지후", "준서",
                "서연", "서윤", "지우", "서현", "하은", "민서", "지유", "채원"]
_COMPANIES = [
    "삼성전자", "SK하이닉스", "LG전자", "현대차", "TSMC Korea",
    "인텔코리아", "마이크론코리아", "엔비디아코리아", "퀄컴코리아", "AMD코리아",
]
_DOMAINS = ["samsung.com", "skhynix.com", "lge.com", "hyundai.com", "corp.co.kr"]


class CustomerGenerator(BaseGenerator):
    COLLECTION = "customers"

    def _make_one(self) -> Customer:
        name = random.choice(_SURNAMES) + random.choice(_GIVEN_NAMES)
        company = random.choice(_COMPANIES)
        phone = f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        email = f"{name}{random.randint(1, 99)}@{random.choice(_DOMAINS)}"
        return Customer(
            id=str(uuid.uuid4()),
            name=name,
            company=company,
            contact=phone,
            email=email,
        )
