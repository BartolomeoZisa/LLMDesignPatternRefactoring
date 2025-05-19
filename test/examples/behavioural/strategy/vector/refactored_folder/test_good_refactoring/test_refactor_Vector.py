import pytest
from refactored.Vector import *

class ReverseSelectionSort(SortStrategy):

    def sort(self, array):
        for i in range(len(array)):
            max_index = i
            for j in range(i + 1, len(array)):
                if array[j] > array[max_index]:  # Reverse condition
                    max_index = j
            array[i], array[max_index] = array[max_index], array[i]

def test_reverse_selection_sort():
    v = Vector()
    for num in [4, 2, 9, 1, 5]:
        v.add(num)

    v.set_sort_strategy(ReverseSelectionSort())
    v.sort()
    
    sorted_result = [v.get(i) for i in range(v.size)]
    assert sorted_result == [9, 5, 4, 2, 1]
