class SortStrategy:
    """Base class for sorting strategies."""
    def sort(self, elements):
        raise NotImplementedError("Sort method not implemented!")

class SelectionSort(SortStrategy):
    """Implementation of selection sort algorithm."""
    def sort(self, elements):
        size = len(elements)
        for i in range(size):
            min_index = i
            for j in range(i + 1, size):
                if elements[j] < elements[min_index]:
                    min_index = j
            elements[i], elements[min_index] = elements[min_index], elements[i]

class Vector:
    """A vector class using strategy pattern for sorting."""
    def __init__(self):
        self.__elements = []
        self.size = 0
        self.__sort_strategy = SelectionSort()  # Default sorting strategy

    def set_sort_strategy(self, sort_strategy):
        """Set a different sorting strategy."""
        if not isinstance(sort_strategy, SortStrategy):
            raise TypeError("Invalid sort strategy!")
        self.__sort_strategy = sort_strategy

    def add(self, element):
        """Add an element to the vector."""
        self.__elements.append(element)
        self.size += 1

    def pop(self):
        """Pop the last element from the vector."""
        if self.size == 0:
            raise IndexError("pop from empty vector")
        self.size -= 1
        return self.__elements.pop()

    def sort(self):
        """Sort the elements using the current sorting strategy."""
        self.__sort_strategy.sort(self.__elements)

    def get(self, index):
        """Get an element at a specific index."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.__elements[index]

    def to_string(self):
        """Get string representation of the vector."""
        return str(self.__elements)
