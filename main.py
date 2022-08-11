import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # The warning is about the potential danger you are introducing by re-using these names at inner scopes. It can cause you to miss a bug. For example, consider this
    #
    # def sample_func(*args):
    #     smaple = sum(args) # note the misspelling of `sample here`
    #     print(sample * sample)
    #
    # if __name__ == "__main__":
    #     for sample in range(1, 5):
    #         sample_func()
    # Because you used the same name, your misspelling inside the function does not cause an error.
    #
    # When your code is very simple, you will get away with this type of thing with no consequences. But it's good to use these "best practices" in order to avoid mistakes on more complex code.

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and # НЕ КРИТИЧНАЯ ОШИБКА, но лучше делать не так, потому что скорость прочтения кода Python(ом) уменьшается
                (today - record.date).days >= 0 # НЕ КРИТИЧНАЯ ОШИБКА, но лучше делать не так, потому что скорость прочтения кода Python(ом) уменьшается
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!') #Здесь скобки не нужны


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # In Python, the names of variables and functions should be lowercase. Individual words can be separated by
    # underscores when needed. This will improve readability within your code. Method names should follow the same
    # conventions as function names.
    #
    # Here are a few best practices' to follow when naming your variables and functions:
    #
    # 1) Constants should be represented by all capital letters and separated by underscores when needed
    # 2) Use names that are representative of the meaning of the object rather than meaningless, single-character names
    # 3) Names i, j, and k should be reserved for representing index values
    # 4) Understanding and adopting these best practices is a great way to polish your coding skills. Writing more
    # elegant code will not only impress your current colleagues, but it will also help you build better
    # coding habits that may catch the attention of future employers.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
