from abc import ABC, abstractmethod


class Vector:

    def __init__(self):
        self.__elements = []
        self.size = 0
        self.set_sort_strategy(SelectionSort())
    
    def add(self, element):
        self.__elements.append(element)
        self.size += 1
    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty vector")
        self.size -= 1
        return self.__elements.pop()
    
    def set_sort_strategy(self, strategy):
        self.sort_strategy = strategy
    
    def sort(self):
        self.sort_strategy.sort(self.__elements)
    
    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.__elements[index]
    
    def to_string(self):
        return str(self.__elements)


class SortStrategy:
    @abstractmethod
    def sort(self, vector):
        pass

class SelectionSort(SortStrategy):

    def sort(self, array):

        for i in range(len(array)):
            min_index = i
            for j in range(i + 1, len(array)):
                if array[j] < array[min_index]:
                    min_index = j
            array[i], array[min_index] = array[min_index], array[i]
        