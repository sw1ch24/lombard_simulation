import random
import time
from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from russian_names import RussianNames
from classes.Human import Human
from classes.Items import *


class Simulation:
    def __init__(self):
        self.__humans = []
        self.__humans_not_client = []
        self.__humans_expired_now = []
        self.__humans_expired_sell = []
        self.__is_running = False
        self.__day = 0
        self.__time_boost = False
        self.__total_profit = 0

    def display(self):
        print(self.__humans, self.__humans_not_client, self.__humans_expired_now, self.__humans_expired_sell,
              self.__is_running, self.__day, self.__time_boost, self.__total_profit)

    def human_gen(self):
        def item_gen():
            gold_items_random = ["Золотой слиток", "Золотое ювелирное изделие", "Золотой лом"]
            gold_standarts_random = [375, 417, 500, 585, 625, 750, 792, 800, 875, 917, 958, 999]
            electronics_random = ["Холодильник", "Варочная плита", "Духовой шкаф", "Кофемашина", "Соковыжималка",
                                  "Микроволновая печь", "Посудомоечная машина", "Стиральная машина", "Телевизор",
                                  "Персональный компьютер", "Пылесос"]
            fur_random = ["Верхняя меховая одежда", "Меховое украшение", "Меховой головной убор", "Меховая галантерея"]

            gold = Gold_Item(random.choice(gold_items_random), random.randint(1,299), random.choice(gold_standarts_random))
            electronic = Electronic_Item(random.choice(electronics_random), random.randint(0,10), random.randint(5000, 100000))
            fur = Fur_Item(random.choice(fur_random), random.randint(1, 15), random.randint(10, 10000), random.randint(0, 99))
            gold.set_cost()
            electronic.set_cost()
            fur.set_cost()
            random_items = [gold, electronic, fur]
            n = random.randint(1, 3)
            if n == 1:
                return random.choice(random_items),
            elif n == 2:
                r1 = random.choice(random_items)
                random_items.remove(r1)
                r2 = random.choice(random_items)
                return r1, r2
            elif n == 3:
                return random_items[0], random_items[1], random_items[2]

        items = item_gen()
        adress = (random.choice(["Антона Петрова, ", "Попова, ", "Малахова, ", "Ленина, ", "Андропова, ", "Воровского, ",
                                "Взлетная, ", "Власихинская, ", "Трактовая, ", "Калинина, ", "Димитрова, ",
                                "Георгиева, ", "Георгия Исакова, ", "Павловский тракт, ", "Петра Сухова, ",
                                "Земляничная, ", "Шукшина, ", "Эмилии Алексеевой, ", "Космонавтов, ",
                                "Сизова, ", "Юрина, ", "Гущина, ", "Матросова, ", "Чкалова, ", "Гоголя, "]) +
                  str(random.randint(1, 199)))
        adress = ''.join(random.choices([adress, "-"], weights=[70, 30]))
        human = Human(RussianNames().get_person(),
                      ''.join([str(random.randint(0,9)) for x in range(6)]),
                      adress, items)
        return human

    def sim(self):
        while self.__is_running:
            self.__day += 1
            output_text.insert(tk.END, f'\nДень №{self.__day}\n')
            sum_cost_day = 0
            profit_day = 0
            expenses_day = 0
            for i in range(random.randint(0, 5)):
                human = self.human_gen()
                items = human.get_items()
                output_text.insert(tk.END, f'\n{human.get_name()} (Номер документа: {human.get_number()}, '
                                           f'адрес: {human.get_address()}) заложил {", ".join([i.get_title() for i in items])}.'
                                           f'\n (Общая оценка залога: {human.sum_cost()}р)')
                output_text.see(tk.END)
                root.update()
                sum_cost_day += human.sum_cost()
                human.set_day_of_bail(self.__day)
                self.__humans.append(human)
            self.__total_profit -= sum_cost_day / 2
            expenses_day += sum_cost_day / 2
            for i in self.__humans:
                w_a = 20
                w_b = 70
                if i.get_amount_of_extensions == 1:
                    w_a -= 10
                    w_b += 10
                elif i.get_amount_of_extensions == 2:
                    w_a -= 15
                    w_b += 15
                elif i.get_amount_of_extensions == 3:
                    w_a -= 20
                    w_b += 20

                if self.__day - i.get_day_of_bail() == 30:
                    i.set_status_of_bail(*random.choices(["Продлен", "Выкуплен", "Просрочен"], weights=[w_a, w_b, 10]))
                    if i.get_status_of_bail() == "Продлен":
                        i.set_day_of_bail(self.__day)
                        temp = (((i.sum_cost() / 2) / 100) * 2) * 30
                        self.__total_profit += temp
                        profit_day += temp

                        output_text.insert(tk.END, f'\n{i.get_name()} (Номер документа: {i.get_number()}, адрес: {i.get_address()}) '
                                                   f'продлил залог, заплатив {round(temp)}p')
                        output_text.see(tk.END)
                        root.update()
                    elif i.get_status_of_bail() == "Выкуплен":
                        i.set_day_of_bail(0)
                        temp = ((((i.sum_cost() / 2) / 100) * 2) * 30) + (i.sum_cost() / 2)
                        self.__total_profit += temp
                        profit_day += temp
                        self.__humans.remove(i)
                        self.__humans_not_client.append(i)

                        output_text.insert(tk.END, f'\n{i.get_name()} (Номер документа: {i.get_number()}, адрес: {i.get_address()}) '
                                                   f'выкупил залог, заплатив {round(temp)}p')
                        output_text.see(tk.END)
                        root.update()
                    elif i.get_status_of_bail() == "Просрочен":
                        i.set_day_of_bail(0)
                        self.__humans.remove(i)
                        self.__humans_expired_now.append(i)

                        output_text.insert(tk.END, f'\n{i.get_name()} (Номер документа: {i.get_number()}, '
                                                   f'адрес: {i.get_address()}) просрочил залог')
                        output_text.see(tk.END)
                        root.update()
            for i in self.__humans_expired_now:
                i.set_day_of_bail(i.get_day_of_bail() + 1)
                is_buyback = "".join(random.choices(["True", "False"], weights=[0.5, 99.5]))
                if is_buyback == "True":
                    i.set_status_of_bail(*random.choices(["Продлен", "Выкуплен"], weights=[15, 85]))
                    self.__humans_expired_now.remove(i)
                    self.__humans.append(i)
                    temp1 = (((i.sum_cost() / 2) / 100) * 5) * i.get_day_of_bail()
                    self.__total_profit += temp1
                    profit_day += temp1
                    output_text.insert(tk.END, f'\n{i.get_name()} (Номер документа: {i.get_number()}, адрес: {i.get_address()}) '
                                       f'оплатил просроченный залог на сумму {round(temp1)}p')
                    output_text.see(tk.END)
                    root.update()
                if i.get_day_of_bail() == 90:
                    temp2 = i.sum_cost()
                    self.__total_profit += temp2
                    profit_day += temp2
                    self.__humans_expired_now.remove(i)
                    self.__humans_expired_sell.append(i)
                    output_text.insert(tk.END, f'\nЗалог клиента {i.get_name()} (Номер документа: {i.get_number()}, адрес: {i.get_address()}) '
                                       f'на сумму {round(temp2)}p был продан')
                    output_text.see(tk.END)
                    root.update()

            output_text.insert(tk.END, f'\n\nИтог дня:\n Доходы: {round(profit_day)}р\n Расходы: {round(expenses_day)}р'
                                       f'\n___________________________________________________________________________'
                                       f'_________________________________________________________________\n')
            output_text.see(tk.END)
            root.update()

            if self.__is_running == False:
                output_text.config(state=DISABLED)
            if self.__time_boost == False:
                time.sleep(0.5)


    def start_sim(self):
        output_text.config(state=NORMAL)
        self.__is_running = True
        simulation_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        stats_button.config(state=tk.DISABLED)
        self.sim()

    def stop_sim(self):
        self.__is_running = False
        simulation_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        stats_button.config(state=tk.NORMAL)

    def time_boost(self):
        if self.__time_boost == True:
            self.__time_boost = False
        else:
            self.__time_boost = True

    def stats(self):
        output_text.config(state=NORMAL)
        output_text.insert(tk.END, f'\nПрофит: {round(self.__total_profit)}\n')
        output_text.see(tk.END)

        expects_pay = []
        extended = []
        bought = self.__humans_not_client
        expired_now = self.__humans_expired_now
        expired_sell = self.__humans_expired_sell
        for i in self.__humans:
            if i.get_status_of_bail() == "Ожидает выкупа":
                expects_pay.append(i)
            elif i.get_status_of_bail() == "Продлен":
                extended.append(i)
        all = len(expects_pay) + len(extended) + len(bought) + len(expired_now) + len(expired_sell)

        output_text.insert(tk.END, f'Статистика по залогам:\n Ожидающих выкупа: {len(expects_pay)}\n'
                                   f' Продленных: {len(extended)}\n Выкупленных: {len(bought)}\n'
                                   f' Просроченных (не проданных): {len(expired_now)}\n'
                                   f' Просроченных (проданных): {len(expired_sell)}\n Всего залогов в базе:{all}')
        output_text.see(tk.END)
        output_text.config(state=DISABLED)


Simulation = Simulation()
root = Tk()
root.title("Ломбард")
root.geometry("1350x850")

output_text = scrolledtext.ScrolledText(root, width=140, height=30, wrap="char", font='Times 13')
output_text.pack(pady=10, expand=False)

simulation_button = tk.Button(root, text="Запустить симуляцию", command=Simulation.start_sim)
simulation_button.pack()

stop_button = tk.Button(root, text="Остановить симуляцию", command=Simulation.stop_sim, state=tk.DISABLED)
stop_button.pack()

boost_button = tk.Button(root, text="Вкл/Выкл ускорение симуляции", command=Simulation.time_boost)
boost_button.pack()

stats_button = tk.Button(root, text="Показать статистику", command=Simulation.stats)
stats_button.pack()

root.mainloop()
