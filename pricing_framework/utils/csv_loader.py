import csv
from pathlib import Path
from typing import Any, Dict, List


class CSVLoader:
    """Загрузчик файлов из CSV-файлов"""

    def __init__(self, file_path: str):
        """Инициализация загрузчика"""
        self.file_path = Path(file_path)

    def load(self) -> List[Dict[str, Any]]:
        """Загружает CSV-файл в список словарей"""

        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def load_as_dict(self, key_column: str) -> Dict[str, List[Dict[str, Any]]]:
        """Загружает CSV-файл и группирует по ключевому столбцу"""

        data = self.load()
        result: Dict[str, List[Dict[str, Any]]] = {}

        for row in data:
            key = row.get(key_column)
            if key:
                if key not in result:
                    result[key] = []
                result[key].append(row)

        return result
