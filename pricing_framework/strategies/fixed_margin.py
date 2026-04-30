"""Стратегия фиксированной маржи"""
from typing import List
from pricing_framework.core.interfaces.product import AbstractProduct
from pricing_framework.core.interfaces.pricing_strategy import AbstractStrategy


class FixedMarginStrategy(AbstractStrategy):
    """Цена = себестоимость + фиксированная наценка в рублях"""

    def __init__(self, margin_amount: float):
        self.margin_amount = margin_amount

    def calculate(self, product: AbstractProduct, competitor_prices: List[float]) -> float:
        return product.get_cost() + self.margin_amount
