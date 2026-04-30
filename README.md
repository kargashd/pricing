# Pricing Framework

Фреймворк для динамического ценообразования на маркетплейсах. Анализирует цены конкурентов из CSV-файла и рекомендует оптимальную цену товара на основе выбранной стратегии.

## Содержание
- [Технологии](#технологии)
- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [Доступные стратегии](#доступные-стратегии)
- [Формат CSV](#формат-csv)
- [Структура проекта](#структура-проекта)
- [Тестирование](#тестирование)
- [Лицензия](#лицензия)
- [Команда проекта](#команда-проекта)

## Технологии
- Python 3.8+
- Pytest
- Flake8
- Black
- Isort
- Mypy
- Setuptools

## Установка

### Установка из GitHub (рекомендуется)


pip install git+https://github.com/kargashd/pricing.git

### Установка в режиме разработки

git clone https://github.com/kargashd/pricing.git
cd pricing
python -m venv .venv
.venv\Scripts\activate  # Windows

### source .venv/bin/activate  # macOS/Linux
pip install -e .

## Быстрый старт

### 1. Подготовьте CSV-файл с ценами конкурентов

```bash
sku,name,competitor,price
IPHONE15_128,iPhone 15 128GB,TechShop,78990
IPHONE15_128,iPhone 15 128GB,MobileStore,79990
IPHONE15_128,iPhone 15 128GB,ElectroCity,81990
IPHONE15_128,iPhone 15 128GB,PhoneMarket,77990
IPHONE15_128,iPhone 15 128GB,GadgetWorld,79500
```

### 2. Запрограммируй код

```bash
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

            monitor = CSVCompetitorMonitor("competitor_prices.csv")

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
```

### 3. Запусти модуль

python my_script.py

### 4. Выберите стратегию

### 5. Вывод:

```bash
Стратегия: Кластеризация конкурентов
Рекомендуемая цена: 78,990 ₽
Прибыль: 13,990 ₽
Маржинальность: 17.71%
Цены конкурентов: [78990.0, 79990.0, 81990.0, 77990.0, 79500.0]
Цена после стратегии: 78990.00 ₽
Себестоимость: 65,000 ₽
```

## Доступные стратегии

### FixedMarginStrategy (Фиксированная наценка)
strategy = FixedMarginStrategy(margin_amount=5000)

### LowerMarginStrategy (Дешевле самого дешёвого конкурента)
strategy = LowerMarginStrategy(offset=500)

### TrendTrackingStrategy (Следование за трендом с базовой корректировкой 3%)
strategy = TrendTrackingStrategy(base_adjustment=0.03)

### ClusterStrategy (Кластеризация конкурентов)
strategy = ClusterStrategy(cluster="mid", adjustment=0)

## Формат CSV

Файл должен содержать следующие колонки:

- `sku` (str) — артикул товара (уникальный идентификатор)
- `name` (str) — наименование товара
- `competitor` (str) — название магазина-конкурента
- `price` (int/float) — цена в рублях

## Структура проекта

```bash
pricing/
├── pricing_framework/
│   ├── core/
│   │   ├── interfaces/           # Абстрактные классы
│   │   │   ├── product.py
│   │   │   ├── pricing_strategy.py
│   │   │   └── competitor_monitor.py
│   │   └── engine.py             # Движок ценообразования
│   ├── domains/
│   │   └── marketplace/
│   │       ├── product.py        # Класс MarketplaceProduct
│   │       └── competitor_monitor.py
│   ├── strategies/               # Стратегии ценообразования
│   │   ├── fixed_margin.py
│   │   ├── lower_margin.py
│   │   ├── trend_tracking.py
│   │   └── cluster_strategy.py
│   └── utils/
│       └── csv_loader.py         # Загрузчик CSV
├── tests/                        # Модульные тесты
├── examples/
│   └── basic_usage.py            # Пример использования
├── data/
│   └── competitor_prices.csv     # Пример данных
├── pyproject.toml                # Конфигурация проекта
├── setup.py                      # Установка пакета
├── requirements.txt              # Зависимости
├── LICENSE                       # MIT лицензия
└── README.md
```

## Тестирование

### Установка зависимостей для разработки
pip install -e .[dev]

### Запуск всех тестов
python -m pytest tests/ -v

### С покрытием кода
python -m pytest tests/ -v --cov=src --cov-report=term-missing

## Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле LICENSE.

## Команда проекта

Daniil Kargashin — разработчик

Email: danilo98.24fevral@yandex.ru

GitHub: kargashd

Проект: github.com/kargashd/pricing