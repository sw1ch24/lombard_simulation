from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, title):
        self.__title = title

    @abstractmethod
    def set_cost(self):
        pass

    def get_title(self):
        return self.__title


class Gold_Item(Item):
    def __init__(self, title, weight, standart):
        super().__init__(title)
        self.__weight = weight
        self.__standart = standart
        self.__cost = 0

    def display(self):
        print(self.__title, self.__weight, self.__standart, self.__cost)

    def set_cost(self):
        if self.__standart > 374 and self.__standart < 586:
            self.__cost = self.__weight * 300
        elif self.__standart < 959:
            self.__cost = self.__weight * 600
        elif self.__standart == 999:
            self.__cost = self.__weight * 1000

    def get_cost(self):
        return self.__cost


class Electronic_Item(Item):
    def __init__(self, title, time_used, cost_new):
        super().__init__(title)
        self.__time_used = time_used
        self.__cost_new = cost_new
        self.__cost = 0

    def display(self):
        print(self.__title, self.__time_used, self.__cost_new, self.__cost)

    def set_cost(self):
        if self.__time_used == 0:
            self.__cost = round(self.__cost_new - (self.__cost_new / 10))
        elif self.__time_used > 0:
            self.__cost = round(self.__cost_new - (self.__time_used * (self.__cost_new / 100 * 7.5)))

    def get_cost(self):
        return self.__cost


class Fur_Item(Item):
    def __init__(self, title, weight, value, wear):
        super().__init__(title)
        self.__weight = weight
        self.__value = value
        self.__wear = wear
        self.__cost = 0

    def display(self):
        print(self.__title, self.__weight, self.__value, self.__wear, self.__cost)

    def set_cost(self):
        if self.__wear == 0:
            self.__cost = round(self.__weight * self.__value)
        elif self.__wear > 0 and self.__wear < 100:
            self.__cost = round(self.__weight * (self.__value - (self.__value / 100 * self.__wear)))


    def get_cost(self):
        return self.__cost