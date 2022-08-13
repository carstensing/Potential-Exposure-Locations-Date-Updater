from datetime import date
from datetime import timedelta

class Date:
    def __init__(self, month_day_year):
        values = month_day_year.split('/')
        self.year = int(values[2])
        self.month = int(values[0])
        self.day = int(values[1])
        if len(values) > 3 or self.day > 31 or self.month > 12 or self.year > 99:
            raise Exception("Date formatted incorrectly") 
    
    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False

        if self.month < other.month:
            return True
        elif self.month > other.month:
            return False

        if self.day < other.day:
            return True

        return False

    def __le__(self, other):
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False

        if self.month < other.month:
            return True
        elif self.month > other.month:
            return False

        if self.day < other.day:
            return True
        elif self.day == other.day and self.month == other.month and self.year == other.year:
            return True

        return False

    def __str__(self):
        return str(self.month) + "/" + str(self.day) + "/" + str(self.year)

    @staticmethod
    def today():
        values = str(date.today()).split('-')
        year = values[0][-2:]
        month = values[1][1] if values[1][0] == '0' else values[1]
        day = values[2][1] if values[2][0] == '0' else values[2]
        return Date(month + "/" + day + "/" + year)

    @staticmethod
    def fourteen_days_ago():
        today = date.today()
        d_14 = timedelta(days=14)
        today_sub_14 = today - d_14
        values = str(today_sub_14).split('-')
        year = values[0][-2:]
        month = values[1][1] if values[1][0] == '0' else values[1]
        day = values[2][1] if values[2][0] == '0' else values[2]
        return Date(month + "/" + day + "/" + year)
