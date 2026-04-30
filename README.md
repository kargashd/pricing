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

sku,name,competitor,price
IPHONE15_128,iPhone 15 128GB,TechShop,78990
IPHONE15_128,iPhone 15 128GB,MobileStore,79990
IPHONE15_128,iPhone 15 128GB,ElectroCity,81990
IPHONE15_128,iPhone 15 128GB,PhoneMarket,77990
IPHONE15_128,iPhone 15 128GB,GadgetWorld,79500

### 2. Запрограммируй код

from pricing_framework import PricingEngine
from pricing_framework.domains.marketplace import MarketplaceProduct, CSVCompetitorMonitor
from pricing_framework.strategies import FixedMarginStrategy

iphone = MarketplaceProduct(
    sku="IPHONE15_128",
    name="iPhone 15 128GB",
    category="Смартфоны",
    brand="Apple",
    cost=65000,
    stock=15
)

monitor = CSVCompetitorMonitor("competitor_prices.csv")

strategy = FixedMarginStrategy(margin_amount=10000)

engine = PricingEngine(strategy, monitor)
price = engine.get_price(iphone)

print(f"Рекомендуемая цена: {price:,.0f} ₽")
print(f"Прибыль: {price - iphone.get_cost():,.0f} ₽")

### 3. Запусти модуль

python my_script.py

Вывод:

Рекомендуемая цена: 7,9990 ₽
Прибыль: 6,4990 ₽

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

### Структура проекта

```bash
pricing/
├── src/
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