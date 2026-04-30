import pytest
import tempfile
import os
from pricing_framework.utils.csv_loader import CSVLoader


class TestCSVLoader:
    def test_load_file_not_found(self):
        loader = CSVLoader("not_exists.csv")
        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_load_success(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,price\nIPHONE,78990\nS24,74990")
            temp_path = f.name

        try:
            loader = CSVLoader(temp_path)
            data = loader.load()

            assert len(data) == 2
            assert data[0]["sku"] == "IPHONE"
            assert data[0]["price"] == "78990"
            assert data[1]["sku"] == "S24"
            assert data[1]["price"] == "74990"
        finally:
            os.unlink(temp_path)

    def test_load_as_dict(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("sku,price\nIPHONE,78990\nIPHONE,79990\nS24,74990")
            temp_path = f.name

        try:
            loader = CSVLoader(temp_path)
            grouped = loader.load_as_dict("sku")

            assert "IPHONE" in grouped
            assert len(grouped["IPHONE"]) == 2
            assert grouped["IPHONE"][0]["price"] == "78990"
            assert grouped["IPHONE"][1]["price"] == "79990"
            assert "S24" in grouped
            assert len(grouped["S24"]) == 1
            assert grouped["S24"][0]["price"] == "74990"
        finally:
            os.unlink(temp_path)
