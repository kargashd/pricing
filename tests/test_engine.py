import pytest
from unittest.mock import Mock
from src.core.engine import PricingEngine
from src.domains.marketplace import MarketplaceProduct


class TestPricingEngine:
    def setup_method(self):
        self.product = MarketplaceProduct(
            sku="TEST",
            name="Test Product",
            category="Test",
            brand="Test",
            cost=65000
        )
        self.mock_strategy = Mock()
        self.mock_monitor = Mock()

    def test_get_price_calls_strategy_and_monitor(self):
        self.mock_monitor.get_prices.return_value = [78990, 79990]
        self.mock_strategy.calculate.return_value = 75000

        engine = PricingEngine(self.mock_strategy, self.mock_monitor)
        price = engine.get_price(self.product)

        self.mock_monitor.get_prices.assert_called_once_with(self.product)
        self.mock_strategy.calculate.assert_called_once_with(
            self.product, [78990, 79990]
        )
        assert price == 75000

    def test_get_price_rounds_result(self):
        self.mock_monitor.get_prices.return_value = [78990, 79990]
        self.mock_strategy.calculate.return_value = 75000.49

        engine = PricingEngine(self.mock_strategy, self.mock_monitor)
        price = engine.get_price(self.product)

        assert price == 75000

    def test_get_price_protects_below_cost(self):
        self.mock_monitor.get_prices.return_value = [78990, 79990]
        self.mock_strategy.calculate.return_value = 60000  # ниже себестоимости

        engine = PricingEngine(self.mock_strategy, self.mock_monitor)
        price = engine.get_price(self.product)

        assert price == 65000

    def test_get_price_with_details(self):
        self.mock_monitor.get_prices.return_value = [78990, 79990]
        self.mock_strategy.calculate.return_value = 75000

        engine = PricingEngine(self.mock_strategy, self.mock_monitor)
        details = engine.get_price_with_details(self.product)

        assert details["price"] == 75000
        assert details["competitor_prices"] == [78990, 79990]
        assert details["strategy_price"] == 75000
        assert details["cost"] == 65000
        # Проверяем с округлением до 2 знаков (как в коде)
        assert details["margin_percent"] == round((75000 - 65000) / 75000 * 100, 2)
