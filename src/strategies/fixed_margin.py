"""Стратегия фиксированной маржи"""
from typing import List
from src.core.interfaces.product import AbstractProduct
from src.core.interfaces.pricing_strategy import AbstractStrategy


class FixedMarginStrategy(AbstractStrategy):
    """Цена = себестоимость + фиксированная наценка в рублях"""

    def __init__(self, margin_amount: float):
        self.margin_amount = margin_amount

    def calculate(self, product: AbstractProduct, competitor_prices: List[float]) -> float:
        return product.get_cost() + self.margin_amount
