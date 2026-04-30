from typing import List
from pricing_framework.core.interfaces.pricing_strategy import AbstractStrategy
from pricing_framework.core.interfaces.product import AbstractProduct


class TrendTrackingStrategy(AbstractStrategy):
    """Стратегия следования за трендом"""

    def __init__(self, base_adjustment: float = 0.02):
        self.base_adjustment = base_adjustment

    def calculate(self, product: AbstractProduct, competitor_prices: List[float]) -> float:
        if not competitor_prices:
            return product.get_cost() * 1.3

        # Средняя цена
        avg_price = sum(competitor_prices) / len(competitor_prices)

        # Разница между максимальной и минимальной цены
        price_range = max(competitor_prices) - min(competitor_prices)

        # Средняя цена относительно максимальной цены
        avg_price_relative = price_range / avg_price

        if avg_price_relative < 0.05:  # Цены очень близки (<5% разброс)
            # Рынок стабилен -> можно добавить наценку
            price = avg_price * (1 + self.base_adjustment)
        elif avg_price_relative > 0.15:  # Цены сильно различаются (>15%)
            # Рынок нестабилен -> цена по минимуму
            price = min(competitor_prices)
        else:
            # Средний разброс -> средняя цена
            price = avg_price

        return max(price, product.get_cost())
