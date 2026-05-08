import random
import uuid

from dummy_generator.generators.base import BaseGenerator
from dummy_generator.models.schemas import Inventory

_SAMPLE_TYPES = [
    "DRAM-DDR5", "DRAM-DDR4", "NAND-Flash-3D", "NAND-Flash-2D",
    "Logic-IC-7nm", "Logic-IC-14nm", "Power-IC-600V", "Power-IC-200V",
    "MOSFET-N채널", "MOSFET-P채널", "SiC-MOSFET", "GaN-HEMT",
]
_LOCATIONS = ["창고-A1", "창고-A2", "창고-B1", "창고-B2", "클린룸-1", "클린룸-2"]
_UNITS = ["개", "LOT", "Wafer"]


class InventoryGenerator(BaseGenerator):
    COLLECTION = "inventory"

    def _make_one(self) -> Inventory:
        return Inventory(
            id=str(uuid.uuid4()),
            sample_type=random.choice(_SAMPLE_TYPES),
            quantity=random.randint(0, 50000),
            unit=random.choice(_UNITS),
            location=random.choice(_LOCATIONS),
        )
