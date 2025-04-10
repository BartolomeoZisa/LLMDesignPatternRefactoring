class Vector:

    def __init__(self):
        self.__elements = []
        self.size = 0
    
    def add(self, element):
        self.__elements.append(element)
        self.size += 1
    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty vector")
        self.size -= 1
        return self.__elements.pop()
    
    
    def sort(self):
        #sort the elements using selection sort
        for i in range(self.size):
            min_index = i
            for j in range(i + 1, self.size):
                if self.__elements[j] < self.__elements[min_index]:
                    min_index = j
            self.__elements[i], self.__elements[min_index] = self.__elements[min_index], self.__elements[i]
    
    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self.__elements[index]
    
    def to_string(self):
        return str(self.__elements)

