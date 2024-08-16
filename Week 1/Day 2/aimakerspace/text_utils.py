import os
from typing import List


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding
        self.metadata = [] #added by YL

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())
            self.metadata.append({"filename": os.path.basename(self.path), "filepath": self.path}) #added by YL

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents_with_metadata(self): #changed name
        self.load()
        #return self.documents
        return [{"text": doc, "metadata": meta} for doc, meta in zip(self.documents, self.metadata)] #changed by YL


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    #def split_texts(self, texts: List[str]) -> List[str]:
    #    chunks = []
    #    for text in texts:
    #        chunks.extend(self.split(text))
    #    return chunks

    def split(self, text: str, metadata: dict[str, str]) -> List[dict[str, str]]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i : i + self.chunk_size]
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_index"] = i // (self.chunk_size - self.chunk_overlap)
            chunks.append({"text": chunk, "metadata": chunk_metadata})
        return chunks
    def split_texts_with_metadata(
        self, documents_with_metadata: List[dict[str, str]]
    ) -> List[dict[str, str]]:
        chunks = []
        for document in documents_with_metadata:
            chunks.extend(self.split(document["text"], document["metadata"]))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    #chunks = splitter.split_texts(loader.documents)
    chunks = splitter.split_texts_with_metadata(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
