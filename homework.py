""""Sprint project: money and calories calc."""

import datetime as dt


class Record:
    """"Class name: Record. Description: the class creates user's records, using
    amount (int), comment (default = 'без комментария')
    and date (datetime.date).
    If user didn't mention the date - the class takes present day."""

    def __init__(self, amount, comment='без комментария', date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            user_date = dt.datetime.strptime(date, '%d.%m.%Y')
            self.date = user_date.date()


class Calculator:
    """" Class: Calculator. Description: the class takes amount of money
    or quantety of calories as limit.
    The class can creates list of users, calculates
    daily statistics (money expenses or calories gained)
    and calculates statistics for last 7 days."""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """"The method "add_record adds" user's records in list."""

        self.records.append(record)

    def get_today_stats(self):
        """"The method "get_today_stats" can calculate statistics for present date by
        compare dates in records to present dates."""

        now = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == now)

    def stat_for_today(self):
        """"The method returns the different between
        limit and expenses for present day and so
        you know you limit."""

        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        """"The method "get_week_stats" can calculate statistics for last 7 days by
        compare dates in records to 7 days ago date and present date."""

        now = dt.date.today()
        week_ago = now - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_ago < record.date and record.date <= now)


class CaloriesCalculator(Calculator):
    """"Class name: CaloriesCalculator. Description:
    the class gives information about
    calories have been eaten for present day and for last 7 days."""

    def get_calories_remained(self):
        balance = self.stat_for_today()
        if balance > 0 and balance < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """"Class name: CashCalculator. Description: Description:
    the class gives information about
    money spent that have been done for present day and for last 7 days."""

    USD_RATE = 72.55
    EURO_RATE = 85.37
    RUB_RATE = 1.0
    currencies = {'usd': ('USD', USD_RATE),
                  'eur': ('Euro', EURO_RATE),
                  'rub': ('руб', RUB_RATE)}

    def get_today_cash_remained(self, currency='rub'):
        """The method get_today_cash_remained takes one necessary
        variable of currency: rub, eur or usd (default = 'rub').
        The method returns available money balance
        for present day in chosen currency.
        If eur or usd was chosen the method
        converts rubles to these currencies."""

        self.currency = currency
        if currency not in self.currencies:
            format = (', '.join(list(self.currencies)))
            return (f'Введеннй формато валют не поддерживается.'
                    f'Введите {format}')
        balance = self.stat_for_today()
        if balance == 0:
            return 'Денег нет, держись'
        balance = round((balance)
                        / self.currencies[currency][1], 2)
        money_format = self.currencies[currency][0]
        if balance > 0:
            return (f'На сегодня осталось '
                    f'{balance} {money_format}')
        else:
            balance = abs(balance)
            return (f'Денег нет, держись: твой долг - '
                    f'{balance} {money_format}')
