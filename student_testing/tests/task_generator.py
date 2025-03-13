import pprint
from random import choice, randint, sample, shuffle


class Task:
    def __init__(self):
        self.task = ''
        self.answer = ''

    def generator_type_1(self):
        # Тип 2. Какое число а, записанное в двоичной системе, удовлетворяет условию 126_8 < а < 581_6?
        data = [
            ['двоичную', bin],
            ['восьмеричную', oct], 
            ['шестнадцатеричную', hex]
                ]
        system = choice(data)
        n = randint(50, 256)
        self.task = f"Переведите десятичное число {n} в {system[0]} систему счисления. Основание системы писать не нужно."
        self.answer = system[1](n)[2:]

    def generator_type_2(self):
        # Тип 2. Какое число а, записанное в двоичной системе, удовлетворяет условию 126_8 < а < 581_6?
        data = [
            ['8', oct], 
            ['16', hex]
        ]
        n = randint(80, 500)
        left = choice(data)
        left_num = left[-1]((n-1))[2:]  # Левое число
        data.remove(left)               # Убрать повторы
        right = choice(data)            # Правое число
        right_num = right[-1](n+1)[2:]
        self.task = f"""Какое число а, записанное в двоичной системе, удовлетворяет условию {left_num}<sub>{left[0]}</sub> < а < {right_num}<sub>{right[0]}</sub>?"""
        self.answer = n

    def generator_type_3(self):
        # Тип 3. Найдите значение выражения
        data = [
            ['2', bin],
            ['8', oct], 
            ['16', hex]
        ]
        operator = [
            '-', '+'
        ]
        n1, n2, n3 = [randint(50, 500) for n in range(3)]   # Числа
        print(n1, n2, n3)
        sn1, sn2, sn3 = [choice(data) for n in range(3)]    # Системы счисления
        oper1 = choice(operator)
        oper2 = choice(operator)
        self.task = f"""Найдите значение выражения{'\n'}{sn1[-1](n1)[2:]}<sub>{sn1[0]}</sub> {oper1} {sn2[-1](n2)[2:]}<sub>{sn2[0]}</sub> {oper2} {sn3[-1](n3)[2:]}<sub>{sn3[0]}</sub>.{'\n'}Ответ запишите в десятичной системе счисления. В ответе укажите только число, без основания системы счисления.
        """
        self.answer = eval(f'{n1} {oper1} {n2} {oper2} {n3}')

    def generator_type_4(self):
        # Тип 4. Выполните вычитание: 11110012 – 11000102.
        # Ответ запишите в двоичной системе счисления. Основание системы писать не нужно.
        data = [
            ['сложение', '+'],
            ['вычитание', '-']
        ]
        nums = [randint(50, 500) for n in range(2)]
        n1, n2 = max(nums), min(nums)
        # print(n1, n2)
        oper = choice(data)
        self.task = f"""Выполните {oper[0]}: {bin(n1)[2:]}<sub>2</sub> {oper[1]} {bin(n2)[2:]}<sub>2</sub>. """
        self.answer = eval(f'{n1} {oper[1]} {n2}')
    
    def generator_type_5(self):
        names = ['Иван', 'Петр', 'Василий', 'Матвей', 'Мария', 'Дарья', 'Наталья', 'Татьяна']
        logics = [('И', 'and'), ('ИЛИ', 'or')]
        not_logics = [('НЕ', 'not'), ('', '')]
        symbol_logs = ['первая', 'вторая', 'третья', 'четвертая']
        alpha_logs = ['гласная', 'согласная']
        alphabet = ['аеёиоуыэюя', 'бвгджзйклмнпрстфхцчшщъь']
        # «а», «б», «в», «г», «д», «е», «ё», «ж», «з», «и», «й», «к», «л», «м», «н», «о», «п», «р», «с», «т», «у», «ф», «х», «ц», «ч», «ш», «щ», «ъ», «ы», «ь», «э», «ю», «я»
        res_logics = [('ЛОЖНО', False), ('ИСТИНА', True)]
        
        res_value = choice(res_logics) # Выбор варианта выражения: ЛОЖНО/ИСТИНА
        # Выбор вариантов выражения
        log1 = choice(not_logics)   # [('НЕ', 'not'), ('', '')]
        indA1 = symbol_logs.index(choice(symbol_logs)) # ['первая', 'вторая', 'третья', 'четвертая']
        
        alpha1 = choice(alpha_logs) # ['гласная', 'согласная']
        log2 = choice(logics)       # [('И', 'and'), ('ИЛИ', 'or')]
        log3 = choice(not_logics)   # [('НЕ', 'not'), ('', '')]
        indA2 = symbol_logs.index(choice(symbol_logs)) # ['первая', 'вторая', 'третья', 'четвертая']
        
        alpha2 = choice(alpha_logs) # ['гласная', 'согласная']
        
        change_names4 = sample(names, 4)
        
        self.task = f"Дано 4 имени: {', '.join(change_names4)}. Для какого количества из приведённых имён высказывание даёт значение '{res_value[0]}':\n"
        self.task += f"{log1[0]} ({symbol_logs[indA1]} буква {alpha1}) {log2[0]} {log3[0]} ({symbol_logs[indA2]} буква {alpha2})"
        
        self.answer = [w for w in change_names4 if 
                       eval(f"{log1[1]} ('{w[indA1].lower()}' in '{alphabet[alpha_logs.index(alpha1)]}') {log2[1]} {log3[1]} ('{w[indA2].lower()}' in '{alphabet[alpha_logs.index(alpha2)]}')")\
                        == res_value[1]]
        



    def get_task(self):
        return self.task

    def get_answer(self):
        return self.answer



if __name__ == '__main__':
    list_task = {}
    task = Task()
    task.generator_type_5()
    print(task.get_task())
    print(task.get_answer())


