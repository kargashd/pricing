from abc import ABC, abstractmethod
from typing import List

from src.core.interfaces.product import AbstractProduct


class AbstractStrategy(ABC):
    """Абстрактный класс стратегии ценообразования"""

    @abstractmethod
    def calculate(
        self, product: AbstractProduct, competitor_prices: List[float]
    ) -> float:
        """Рассчитать оптимальную цену на основе товара и цен конкурента"""
        pass
