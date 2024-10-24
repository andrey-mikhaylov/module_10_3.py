import random
import time
import threading


class Bank:
    def __init__(self, balance: int=0):
        """
        :param balance: баланс банка
        """
        self.balance = balance

        # объект класса Lock для блокировки потоков.
        self.withdraw_lock = threading.Lock()

        # объект класса Lock для атомарного изменения баланса
        self.balance_lock = threading.Lock()

    def deposit_money(self, money: int):
        """
        Пополнение баланса
        :param money: сумма пополнения
        """
        with self.balance_lock:
            self.balance += money
            new_balance = self.balance
        print(f"Пополнение: {money}. Баланс: {new_balance}\n", end='')

        if self.balance >= 500 and self.withdraw_lock.locked():
            self.withdraw_lock.release()

        time.sleep(0.001)

    def take_money_or_cancel(self, money: int):
        """
        Снятие средств с баланса.
        Если средств недостаточно, запрос будет отклонён, но поток всё равно будет ждать достаточных средств
        :param money: сумма запроса на снятие
        """
        print(f"Запрос на {money}\n", end='')

        if money > self.balance:
            print("Запрос отклонён, недостаточно средств\n", end='')
            self.withdraw_lock.acquire()
        else:
            with self.balance_lock:
                self.balance -= money
                new_balance = self.balance
            print(f"Снятие: {money}. Баланс: {new_balance}\n", end='')

    def deposit(self):
        """
        Будет совершать 100 транзакций пополнения средств.
        """
        for n in range(100):
            money = random.randint(50, 500)
            self.deposit_money(money)

    def take(self):
        """
        Будет совершать 100 транзакций снятия.
        """
        for n in range(100):
            money = random.randint(50, 500)
            self.take_money_or_cancel(money)


def test():
    bk = Bank()
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print(f'Итоговый баланс: {bk.balance}')

    """
    Вывод на консоль (может отличаться значениями, логика должна быть та же):
    Пополнение: 241. Баланс: 241
    Запрос на 174
    Снятие: 174. Баланс: 67
    Пополнение: 226. Баланс: 293
    Запрос на 421
    Запрос отклонён, недостаточно средств
    Пополнение: 133. Баланс: 426
    Запрос на 422
    Снятие: 422. Баланс: 4
    Пополнение: 150. Баланс: 154
    Запрос на 207
    Запрос отклонён, недостаточно средств
    ....
    Запрос на 431
    Снятие: 431. Баланс: 276
    Запрос на 288
    Запрос отклонён, недостаточно средств
    Итоговый баланс: 276
    """


if __name__ == '__main__':
    test()


"""
2023/12/11 00:00|Домашнее задание по теме "Блокировки и обработка ошибок"
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.
Цель: освоить блокировки потоков, используя объекты класса Lock и его методы.

Задача "Банковские операции":
Необходимо создать класс Bank со следующими свойствами:

Атрибуты объекта:
balance - баланс банка (int)
lock - объект класса Lock для блокировки потоков.

Методы объекта:
Метод deposit:
Будет совершать 100 транзакций пополнения средств.
Пополнение - это увеличение баланса на случайное целое число от 50 до 500.
Если баланс больше или равен 500 и замок lock заблокирован - lock.locked(), то разблокировать его методом release.
После увеличения баланса должна выводится строка "Пополнение: <случайное число>. Баланс: <текущий баланс>".
Также после всех операций поставьте ожидание в 0.001 секунды, тем самым имитируя скорость выполнения пополнения.
Метод take:
Будет совершать 100 транзакций снятия.
Снятие - это уменьшение баланса на случайное целое число от 50 до 500.
В начале должно выводится сообщение "Запрос на <случайное число>".
Далее производится проверка: если случайное число меньше или равно текущему балансу, то произвести снятие, уменьшив balance на соответствующее число и вывести на экран "Снятие: <случайное число>. Баланс: <текущий баланс>".
Если случайное число оказалось больше баланса, то вывести строку "Запрос отклонён, недостаточно средств" и заблокировать поток методом acquire.
Далее создайте объект класса Bank и создайте 2 потока для его методов deposit и take. Запустите эти потоки.
После конца работы потоков выведите строку: "Итоговый баланс: <баланс объекта Bank>".

По итогу вы получите скрипт разблокирующий поток до баланса равному 500 и больше или блокирующий, когда происходит попытка снятия при недостаточном балансе.
Пример результата выполнения программы:
Исходный код:
class Bank:
def __init__(self):
....
def deposit(self):
...
def take(self):
...

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')

Вывод на консоль (может отличаться значениями, логика должна быть та же):
Пополнение: 241. Баланс: 241
Запрос на 174
Снятие: 174. Баланс: 67
Пополнение: 226. Баланс: 293
Запрос на 421
Запрос отклонён, недостаточно средств
Пополнение: 133. Баланс: 426
Запрос на 422
Снятие: 422. Баланс: 4
Пополнение: 150. Баланс: 154
Запрос на 207
Запрос отклонён, недостаточно средств
....
Запрос на 431
Снятие: 431. Баланс: 276
Запрос на 288
Запрос отклонён, недостаточно средств
Итоговый баланс: 276

Примечания:
Для генерации случайного целого числа используйте функцию randint из модуля random.
Для ожидания используйте функцию sleep из модуля time.
Особо важно соблюсти верную блокировку: в take замок закрывается, в deposit открывается.
Файл module_10_3.py загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
"""
