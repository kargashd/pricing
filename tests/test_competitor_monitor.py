import pytest
import tempfile
import os
from pricing_framework.domains.marketplace import CSVCompetitorMonitor, MarketplaceProduct


class TestCSVCompetitorMonitor:
    def setup_method(self):
        self.product = MarketplaceProduct(
            sku="IPHONE15_128",
            name="iPhone 15",
            category="Смартфоны",
            brand="Apple",
            cost=65000
        )

    def test_get_prices_existing_sku(self):
        # Создаём временный CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,name,competitor,price\n")
            f.write("IPHONE15_128,iPhone 15,TechShop,78990\n")
            f.write("IPHONE15_128,iPhone 15,MobileStore,79990\n")
            f.write("S24_256,Samsung S24,TechShop,74990\n")
            temp_path = f.name

        try:
            monitor = CSVCompetitorMonitor(temp_path)
            prices = monitor.get_prices(self.product)

            assert len(prices) == 2
            assert 78990 in prices
            assert 79990 in prices
        finally:
            os.unlink(temp_path)

    def test_get_prices_non_existing_sku(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,name,competitor,price\n")
            f.write("IPHONE15_128,iPhone 15,TechShop,78990\n")
            temp_path = f.name

        try:
            monitor = CSVCompetitorMonitor(temp_path)
            unknown_product = MarketplaceProduct(
                sku="UNKNOWN",
                name="Unknown",
                category="Test",
                brand="Test",
                cost=50000
            )
            prices = monitor.get_prices(unknown_product)

            assert prices == []
        finally:
            os.unlink(temp_path)

    def test_get_prices_empty_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,name,competitor,price\n")
            temp_path = f.name

        try:
            monitor = CSVCompetitorMonitor(temp_path)
            prices = monitor.get_prices(self.product)

            assert prices == []
        finally:
            os.unlink(temp_path)

    def test_get_prices_file_not_found(self):
        monitor = CSVCompetitorMonitor("not_exists.csv")
        # Не должно быть ошибки, просто пустой список
        prices = monitor.get_prices(self.product)
        assert prices == []

    def test_refresh(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,name,competitor,price\n")
            f.write("IPHONE15_128,iPhone 15,TechShop,78990\n")
            temp_path = f.name

        try:
            monitor = CSVCompetitorMonitor(temp_path)
            prices_before = monitor.get_prices(self.product)
            assert prices_before == [78990]

            # Перезаписываем файл с новыми данными
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write("sku,name,competitor,price\n")
                f.write("IPHONE15_128,iPhone 15,TechShop,79990\n")
                f.write("IPHONE15_128,iPhone 15,MobileStore,80990\n")

            # Обновляем
            monitor.refresh()
            prices_after = monitor.get_prices(self.product)

            assert len(prices_after) == 2
            assert 79990 in prices_after
            assert 80990 in prices_after
        finally:
            os.unlink(temp_path)

    def test_get_prices_ignores_invalid_prices(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,name,competitor,price\n")
            f.write("IPHONE15_128,iPhone 15,TechShop,78990\n")
            f.write("IPHONE15_128,iPhone 15,MobileStore,invalid\n")
            f.write("IPHONE15_128,iPhone 15,ElectroCity,\n")
            f.write("IPHONE15_128,iPhone 15,PhoneMarket,-100\n")
            temp_path = f.name

        try:
            monitor = CSVCompetitorMonitor(temp_path)
            prices = monitor.get_prices(self.product)

            # Должна быть только одна корректная цена
            assert prices == [78990]
        finally:
            os.unlink(temp_path)
