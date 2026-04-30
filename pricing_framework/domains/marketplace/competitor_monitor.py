from pathlib import Path
from typing import List

from pricing_framework.core.interfaces.competitor_monitor import AbstractMonitor
from pricing_framework.core.interfaces.product import AbstractProduct
from pricing_framework.utils.csv_loader import CSVLoader


class CSVCompetitorMonitor(AbstractMonitor):
    """Мониторинг конкурентов из CSV-файла"""

    def __init__(self, file_path: str):
        """Инициализация мониторинга"""
        self.file_path = Path(file_path)
        self._loader = CSVLoader(str(self.file_path))
        self._data_by_sku: dict = {}
        self._load_data()

    def _load_data(self) -> None:
        """Загрузить и подготовить данные из CSV"""
        try:
            grouped = self._loader.load_as_dict(key_column="sku")

            for sku, rows in grouped.items():
                prices = []
                for row in rows:
                    try:
                        price = float(row.get("price", 0))
                        if price > 0:
                            prices.append(price)
                    except (TypeError, ValueError):
                        continue

                self._data_by_sku[sku] = prices

        except FileNotFoundError:
            self._data_by_sku = {}

    def get_prices(self, product: AbstractProduct) -> List[float]:
        """Получить цены конкурентов для товара"""

        sku = product.get_sku()
        return self._data_by_sku.get(sku, [])

    def refresh(self) -> None:
        """Принудительно обновить данные из CSV"""

        self._load_data()
