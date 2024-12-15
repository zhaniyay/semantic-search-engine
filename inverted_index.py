from __future__ import annotations
import json
import re
from typing import Dict, List


class InvertedIndex:
    def __init__(self, index: Dict[str, List[int]]):
        self.index=index

    def query(self, words: List[str]) -> List[int]:
        """Return the list of relevant documents for the given query"""
        result = None
        for word in words:
            doc_ids = self.index.get(word, [])
            if result is None:
                result = set(doc_ids)
            else:
                result &= set(doc_ids)
        return sorted(result) if result else[]
    
    def dump(self, filepath: str) -> None:
        with open(filepath, "w") as f:
            json.dump(self.index, f)


    @classmethod
    def load(cls, filepath: str) -> InvertedIndex:
        with open(filepath, "r") as f:
            index = json.load(f)
        return cls(index)


def load_documents(filepath: str) -> Dict[int, str]:
    documents = {}
    with open(filepath, "r") as f:
        for line in f:
            doc_id, content = line.strip().split("\t", 1)
            documents[int(doc_id)] = content
    return documents


def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    index = {}
    for doc_id, content in documents.items():
        words = re.split(r"\W+", content.lower())
        for word in words:
            if word:  # Skip empty strings
                index.setdefault(word, []).append(doc_id)
                index[word] = list(set(index[word]))  # Remove duplicates
    return InvertedIndex(index)


def main():
    input_filepath = "/Users/macbookpro/Desktop/bdt_hw_1.0/wikipedia_sample"
    output_index_path = "inverted_index.json"

    documents = load_documents(input_filepath)
    print("Документы загружены:", documents)

    inverted_index = build_inverted_index(documents)
    print("Инвертированный индекс построен.")

    inverted_index.dump(output_index_path)
    print(f"Индекс сохранен в файл: {output_index_path}")

    loaded_index = InvertedIndex.load(output_index_path)
    print("Индекс загружен из файла.")

    query_words = ["two", "words"]
    document_ids = loaded_index.query(query_words)
    print(f"Документы, содержащие слова {query_words}: {document_ids}")


if __name__ == "__main__":
    main()
