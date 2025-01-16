import db
from db.mathdb import MathDatabase

dbMath = MathDatabase('db/mathdb.db')

class MathModule:

    def first_chapter(city, weight, product):
        raz = 0
        res = 0
        weight = float(weight)
        print(weight)
        if 12 <= weight <= 125:
            res = MathModule.calculate_size(weight, 12, 125, 2, 3)
        elif 250 <= weight <= 1000:
            res = MathModule.calculate_size(weight, 250, 1000, 3.5, 4.5)
        elif 1500 <= weight <= 5000:
            res = MathModule.calculate_size(weight, 1500, 5000, 5, 6)
        else:
            raise ValueError("Вес выходит за допустимые пределы.")

    def calculate_size(weight, min_weight, max_weight, min_size, max_size):
        size_range = max_size - min_size
        weight_range = max_weight - min_weight

        ratio = size_range / weight_range

        size = min_size + (weight - min_weight) * ratio

        return round(size, 2)