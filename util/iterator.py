from typing import List, Any


class CustomIterator:
    def __init__(self, collection: List):
        self.collection: List = collection
        self.index = 0

    def next(self) -> None:
        self.index = (self.index + 1) % len(self.collection)

    def previous(self) -> None:
        self.index = (self.index - 1) % len(self.collection)

    def get(self) -> Any:
        return self.collection[self.index]

    def __iter__(self):
        return self

    def __next__(self):
        self.next()
        return self.get()
