class SortStrategy:
    def sort(self, elements):
        raise NotImplementedError("You should implement this method!")


class SelectionSort(SortStrategy):
    def sort(self, elements):
        size = len(elements)
        for i in range(size):
            min_index = i
            for j in range(i + 1, size):
                if elements[j] < elements[min_index]:
                    min_index = j
            elements[i], elements[min_index] = elements[min_index], elements[i]


class Vector:
    
    def __init__(self):
        self.__elements = []
        self.size = 0
        self.sort_strategy = SelectionSort()

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