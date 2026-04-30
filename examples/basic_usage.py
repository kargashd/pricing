import logging
from pricing_framework.domains.marketplace import MarketplaceProduct, CSVCompetitorMonitor
from pricing_framework.strategies import FixedMarginStrategy, LowerMarginStrategy, TrendTrackingStrategy, ClusterStrategy
from pricing_framework.core import PricingEngine

logging.basicConfig(level=logging.INFO)

strategies = [
                {"name": "Фиксированная маржа",
                 "class": FixedMarginStrategy,
                 "params": {"margin_amount": 500}},

                {"name": "Нижний порог",
                 "class": LowerMarginStrategy,
                 "params": {"offset": 500}},

                {"name": "Следуем за трендом",
                 "class": TrendTrackingStrategy,
                 "params": {"base_adjustment": 0.02}},

                {"name": "Кластеризация конкурентов",
                 "class": ClusterStrategy,
                 "params": {"cluster": "mid", "adjustment": 0}},
              ]


def main():
    for i, strat in enumerate(strategies, 1):
        print(f"{i}. {strat['name']}")

    while True:
        try:
            choice = input("Выберите стратегию: ")

            if not choice.isdigit():
                raise ValueError(f"Введите верный номер стратегии: 1-{len(strategies)}")

            choice = int(choice)

            if choice < 1 or choice > len(strategies):
                raise ValueError(f"Введите верный номер стратегии: 1-{len(strategies)}")

            iphone = MarketplaceProduct(
                sku="IPHONE15_128",
                name="iphone 15 128 GB",
                category="Смартфоны",
                brand="Apple",
                cost=65000,
                stock=15
            )

            selected = strategies[choice - 1]

            monitor = CSVCompetitorMonitor("data/competitor_prices.csv")

            strategy = selected["class"](**selected["params"])
            engine = PricingEngine(strategy, monitor)

            details = engine.get_price_with_details(iphone)

            print(f"\nСтратегия: {selected['name']}")
            print(f"Рекомендуемая цена: {details['price']:,.0f} ₽")
            print(f"Прибыль: {details['price'] - details['cost']:,.0f} ₽")
            print(f"Маржинальность: {details['margin_percent']}%")
            print(f"Цены конкурентов: {details['competitor_prices']}")
            print(f"Цена после стратегии: {details['strategy_price']:.2f} ₽")
            print(f"Себестоимость: {details['cost']:,.0f} ₽")

            break

        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
