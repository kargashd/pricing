from abc import ABC, abstractmethod
from typing import List

from src.core.interfaces.product import AbstractProduct

class AbstractMonitor(ABC):
    """Абстрактный класс мониторинга конкуретнов"""

    @abstractmethod
    def get_prices(self, product: AbstractProduct) -> List[float]:
        """Получить цены конкурентов для заданного товара в списке"""
        pass