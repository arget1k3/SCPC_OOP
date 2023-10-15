import sqlite3

class Menu:
    # класс для вызова меню нашей программы

    def main_menu(self):
        print('''Главное меню 📋:
1. Проекты
2. Договоры
9. Просмотреть все договора и проекты
4. Завершить работу с программой''')

    def treaty_menu(self):
        print('''Меню договора 🤝
1. Создать договор
2. Подтвердить договор
3. Завершить договор
9. Просмотреть все договора и проекты
4. ◀️''')

    def create_treaty_menu(self):
        print('''WARNING:(По умолчанию договор будет иметь статус черновика,
Чтобы его активировать - перейдите в пункт "договор"-"подтвердить договор")
Введите название договора''')
        return input()

    def project_menu(self):
        print('''Меню проекта 📄:
1. Создать проект
2. Добавить договор в проект
3. Завершить договор
9. Просмотреть все договора и проекты
4. ◀️''')

    def create_project_menu(self):
        print('''WARNING:(По умолчанию проект не будет иметь договора.
Чтобы добавить договор - перейдите в пункт "проекты"-"добавить договор")
Введите название проекта''')
        return input()

    # возвращает число с типом данных integer start
    @classmethod
    def check_num(cls, item):
        while True:
            try:
                if 0 <= int(item):
                    return int(item)
            except:
                print('Введите число из представленного списка')
                item = input()
    # возвращает число с типом данных integer end

    # меню позволяет просмотреть все проекта и все договора start
    @classmethod
    def take_all(cls):
        print('''1. Просмотреть все проекты
2. Просмотреть все договоры''')
        x = cls.check_num(input())
        if x == 1:
            conn = sqlite3.connect('project.sql')  # подключаем бд
            cur = conn.cursor()
            cur.execute('SELECT * FROM project')  # выбираем все
            treats = cur.fetchall()  # сохраняем данные в переменную
            info = ''
            for el in treats:
                # выводим все проекты
                info += f'{el[0]}: [название проекта: {el[1]}, дата создания: {el[2]}, активный договор: {"Неуказан" if el[3]==None else el[3]}, неактивные договоры: {"Пока нет ни одного неактивного договора" if el[4] == None else el[4]}]\n'
            cur.close()
            conn.close()
            return info
        elif x == 2:
            conn = sqlite3.connect('treaty.sql')  # подключаем бд
            cur = conn.cursor()
            # выбираем все
            cur.execute('SELECT * FROM treaty')
            treats = cur.fetchall()  # сохраняем данные в переменную
            info = ''
            for el in treats:
                # выводим все договоры "Неуказан" if el[5]==None else
                info += f'{el[0]}: [название договора: {el[1]}, дата создания: {el[2]}, дата подписания: {"Неподписан" if el[3] is None else el[3]}, статус: {"Неуказан" if el[4]==None else "Активен" if el[4]=="True" else "Завершен"}, проект: {"Неуказан" if el[5]==None else el[5]}]\n'
            cur.close()
            conn.close()
            return info
        
    # вызов всех функций start
    @staticmethod
    def project_treaty(): 
        print(Menu.take_all()) # m.take_all()
        print('Нажмите на любую клавишу для выхода')
        input()
    # вызов всех функций end

    # меню позволяет просмотреть все проекта и все договора end