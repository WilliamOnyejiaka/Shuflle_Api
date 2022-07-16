import math
import random

def shuffle(str):
    str = list(str)
    [currentIndex,randomIndex,tempValue] = [len(str)-1,None,None]

    while currentIndex > 0 :
        randomIndex = random.randint(0,currentIndex)
        tempValue = str[randomIndex]
        str[randomIndex] = str[currentIndex]
        str[currentIndex] = tempValue
        currentIndex -= 1

    return ''.join(str)


# shuffled:str = shuffle("hello")
# print(shuffled)

class PyShuffle:

    def __init__(self,word) -> None:
        self.word_list = list(word)
        self.current_index = len(self.word_list)-1
        self.random_index = None
        self.temp_value = None
    
    def shuffle(self)-> str:
        while self.current_index > 0:
            self.random_index = random.randint(0,self.current_index)
            self.temp_value = self.word_list[self.random_index]
            self.word_list[self.random_index] = self.word_list[self.current_index]
            self.word_list[self.current_index] = self.temp_value
            self.current_index -= 1
        return self.list_to_str()

    def list_to_str(self):
        return ''.join(self.word_list)
