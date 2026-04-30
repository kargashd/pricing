from setuptools import setup, find_packages

setup(
    name="pricing-framework",
    version="0.1.0",
    author="Daniil Kargashin",
    description="Фреймворк для динамического ценообразования на маркетплейсах",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)