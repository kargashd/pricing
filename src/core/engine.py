import logging
from src.core.interfaces.product import AbstractProduct
from src.core.interfaces.pricing_strategy import AbstractStrategy
from src.core.interfaces.competitor_monitor import AbstractMonitor

logger = logging.getLogger(__name__)


class PricingEngine:
    """Движок ценообразования"""

    def __init__(self, strategy: AbstractStrategy, monitor: AbstractMonitor):
        self.strategy = strategy
        self.monitor = monitor
        logger.info(f"PricingEngine инициализирован со стратегией {strategy.__class__.__name__}")

    def get_price(self, product: AbstractProduct) -> float:
        """Вернуть рекомендованную цену"""
        competitor_prices = self.monitor.get_prices(product)
        price = self.strategy.calculate(product, competitor_prices)
        price = round(price)

        if price < product.get_cost():
            price = product.get_cost() # Продаём по себестоимости

        return price

    def get_price_with_details(self, product: AbstractProduct) -> dict:
        """Вернуть цену с деталями расчёта"""
        competitor_prices = self.monitor.get_prices(product)
        strategy_price = self.strategy.calculate(product, competitor_prices)
        final_price = round(strategy_price)
        cost = product.get_cost()

        if final_price < cost:
            final_price = cost

        margin = (final_price - cost) / final_price * 100 if final_price > 0 else 0

        return {
            "price": final_price,
            "competitor_prices": competitor_prices,
            "strategy_price": strategy_price,
            "cost": cost,
            "margin_percent": round(margin, 2),
        }
