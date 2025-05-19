from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class SelectionSortStrategy(SortStrategy):
    def sort(self, data):
        n = len(data)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if data[j] < data[min_index]:
                    min_index = j
            data[i], data[min_index] = data[min_index], data[i]
        return data

class Vector:
    def __init__(self, sort_strategy=None):
        self.__elements = []
        self.size = 0
        self.__sort_strategy = sort_strategy if sort_strategy else SelectionSortStrategy()

    def add(self, element):
        self.__elements.append(element)
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty vector")
        self.size -= 1
        return self.__elements.pop()

    def sort(self):
        self.__elements = self.__sort_strategy.sort(self.__elements)

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.__elements[index]

    def to_string(self):
        return str(self.__elements)

    def set_sort_strategy(self, sort_strategy):
        self.__sort_strategy = sort_strategy
