import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from app.models.book import Book


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializeStrategy(SerializeStrategy):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializeStrategy(SerializeStrategy):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


class SerializeService:
    def __init__(self, strategy: SerializeStrategy):
        self.strategy = strategy

    def serialize(self, book: Book) -> str:
        return self.strategy.serialize(book)


class SerializeStrategyFactory:
    @staticmethod
    def create(strategy_type: str) -> SerializeStrategy:
        strategies = {
            "json": JsonSerializeStrategy,
            "xml": XmlSerializeStrategy,
        }
        strategy_class = strategies.get(strategy_type)
        if strategy_class is None:
            raise ValueError(f"Unknown serialize type: {strategy_type}")
        return strategy_class()
