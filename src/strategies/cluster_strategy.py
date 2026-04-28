from typing import List
from src.core.interfaces.pricing_strategy import AbstractStrategy
from src.core.interfaces.product import AbstractProduct


class ClusterStrategy(AbstractStrategy):
    """Кластеризация конкурентов"""

    def __init__(self, cluster: str = "mid", adjustment: float = 0):
        valid_clusters = ["low", "mid", "high"]
        if cluster not in valid_clusters:
            raise ValueError(f"cluster должен быть: {valid_clusters}")

        self.cluster = cluster
        self.adjustment = adjustment

    def calculate(self, product: AbstractProduct, competitor_prices: List[float]) -> float:
        if not competitor_prices:
            return product.get_cost() * 1.3

        # Сортируем цены
        sorted_prices = sorted(competitor_prices)
        n = len(sorted_prices)

        # Делим на 3 кластера
        low_size = n // 3
        mid_size = n // 3

        low_cluster = sorted_prices[:low_size]
        mid_cluster = sorted_prices[low_size:low_size + mid_size]
        high_cluster = sorted_prices[low_size + mid_size:]

        # Выбираем нужный кластер
        if self.cluster == "low":
            cluster_prices = low_cluster
        elif self.cluster == "mid":
            cluster_prices = mid_cluster
        else:  # high
            cluster_prices = high_cluster

        # Средняя цена в кластере
        avg_cluster_price = sum(cluster_prices) / len(cluster_prices)

        # Применяем корректировку
        price = avg_cluster_price + self.adjustment

        # Защита от цены ниже себестоимости
        return max(price, product.get_cost())
