import datetime
import calendar

days_passed = float(datetime.date.today().strftime('%j'))
current_year = datetime.date.today().year

if calendar.isleap(current_year):
    year_progress = days_passed/366
else:
    year_progress = days_passed/365

if __name__ == '__main__':
    print(year_progress)
