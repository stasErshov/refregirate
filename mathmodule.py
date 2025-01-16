import math

from db.mathdb import MathDatabase

dbMath = MathDatabase('db/mathdb.db')

class MathModule:

    def first_chapter(city, weight, product):
        res_list = []
        weight = float(weight)
        print(weight)
        if 12 <= weight <= 125:
            res = MathModule.calculate_size(weight, 12, 125, 2, 3)
        elif 250 <= weight <= 1000:
            res = MathModule.calculate_size(weight, 250, 1000, 3.5, 4.5)
        elif 1500 <= weight <= 5000:
            res = MathModule.calculate_size(weight, 1500, 5000, 5, 6)

        load = dbMath.search_product(product)
        load = MathModule.find_max_in_column(load, 2)

        res_list.append(round(weight / (0.75 * res * load[2]), 2))
        res_list.append(round(0.25 * res_list[0], 2))
        res_list.append(round(res_list[1] + res_list[0], 2))
        res_list.append(round(0.05 * res_list[2], 2))
        res_list.append(round(0.2 * res_list[2], 2))
        for i in res_list:
            print(math.ceil(i / 144))
        return True

    def calculate_size(weight, min_weight, max_weight, min_size, max_size):
        size_range = max_size - min_size
        weight_range = max_weight - min_weight

        ratio = size_range / weight_range

        size = min_size + (weight - min_weight) * ratio

        return round(size, 2)

    def find_max_in_column(matrix, column_index):
        max_float = None
        max_index = None

        # Проходим по списку с использованием enumerate для доступа к индексам
        for i, item in enumerate(matrix):
            current_float = item[column_index]  # Получаем float-значение из тройки

            if max_float is None or current_float > max_float:
                max_float = current_float
                max_index = matrix[i]

        return max_index