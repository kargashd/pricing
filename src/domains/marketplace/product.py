from typing import Optional

from src.core.interfaces.product import AbstractProduct


class MarketplaceProduct(AbstractProduct):
    """Продукт для маркетплейса (смартфоны, электроника)"""

    def __init__(
        self,
        sku: str,
        name: str,
        category: str,
        brand: str,
        cost: float,
        current_price: Optional[float] = None,
        stock: int = 0,
    ):
        self._sku = sku
        self._name = name
        self.category = category
        self.brand = brand
        self._cost = cost
        self.current_price = current_price
        self.stock = stock

    def get_sku(self) -> str:
        return self._sku

    def get_name(self) -> str:
        return self._name

    def get_category(self) -> str:
        return self.category

    def get_brand(self) -> str:
        return self.brand

    def get_cost(self) -> float:
        return self._cost

    def get_current_price(self) -> Optional[float]:
        return self.current_price

    def get_stock(self) -> int:
        return self.stock

    def __repr__(self) -> str:
        return (
            f"MarketplaceProduct("
            f"sku={self._sku}, "
            f"name={self._name}, "
            f"category={self.category}, "
            f"brand={self.brand}, "
            f"cost={self._cost}, "
            f"stock={self.stock})"
        )
