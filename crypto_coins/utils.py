# функция для округления разных порядков чисел
def round_number(number):
    if not number:
        return False
    elif number < 0:
        return round(number, 2)
    elif number < 0.001:
        return round(number, 6)
    elif number < 0.01:
        return round(number, 6)
    elif number < 0.1:
        return round(number, 5)
    elif number < 1:
        return round(number, 4)
    elif number < 10:
        return round(number, 3)
    elif number >= 10:
        return round(number, 2)
    

