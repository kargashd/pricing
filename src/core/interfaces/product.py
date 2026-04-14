from abc import ABC, abstractmethod

class AbstractProduct(ABC):
    """Абстрактный класс продукта"""

    @abstractproduct
    def get_sku(self) -> str:
        """Уникальный идентификатор товара"""
        pass

    @abstractmethod
    def get_name(self) -> str
        """Название товара"""
        pass

    @abstractmethod
    def get_cost(self) -> float:
        """Себестоимость товара"""
        pass