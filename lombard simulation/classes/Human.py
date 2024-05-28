class Human:
    def __init__(self, name, number, address, items):
        self.__name = name
        self.__number = number
        self.__address = address

        self.__items = items
        self.__day_of_bail = 0
        self.__status_of_bail = "Ожидает выкупа"
        self.__amount_of_extensions = 0

    def display(self):
        print(self.__name, self.__number, self.__address, self.__items, self.__day_of_bail, self.__status_of_bail,
               self.__amount_of_extensions)

    def sum_cost(self):
        return sum([i.get_cost() for i in self.__items])

    def set_day_of_bail(self, day_of_bail):
        self.__day_of_bail = day_of_bail

    def set_status_of_bail(self, status_of_bail):
        self.__status_of_bail = status_of_bail

    def set_amount_of_extensions(self, amount_of_extensions):
        self.__amount_of_extensions = amount_of_extensions

    def get_amount_of_extensions(self):
        return self.__amount_of_extensions

    def get_status_of_bail(self):
        return self.__status_of_bail

    def get_day_of_bail(self):
        return self.__day_of_bail

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_address(self):
        return self.__address

    def get_items(self):
        return self.__items
