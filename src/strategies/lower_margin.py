from typing import List
from src.core.interfaces.pricing_strategy import AbstractStrategy
from src.core.interfaces.product import AbstractProduct


class LowerMarginStrategy(AbstractStrategy):
    """Цена = минимальная цена конкурентов - твоя корректировка"""

    def __init__(self, offset: float):
        self.offset = offset

    def calculate(self, product: AbstractProduct, competitor_prices: List[float]) -> float:
        return min(competitor_prices) - self.offset
