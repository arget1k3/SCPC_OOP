import sqlite3
from datetime import *

class Project:
    # класс для работы с проектами

    # создание бд start
    def __init__(self, project):
        self.project = project  # делаем проверку нашего значения
        conn = sqlite3.connect('project.sql')  # создаем бд
        cur = conn.cursor()
        # создаем таблицу
        cur.execute('CREATE TABLE IF NOT EXISTS project (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50), date_sign varchar(10), treaty varchar(50), inactive_treaty varchar(50))')
        self.check_name(project)
        cur.execute('INSERT INTO project (name, date_sign) VALUES (?, ?)', (self.project,
                    date.today().strftime("%d.%m.%Y")))  # добавляем в таблицу название проекта
        conn.commit()  # подтверждаем действие
        cur.close()
        conn.close()  # закрываем таблицу
        print('Проект успешно создан ✅')
    # создание бд end

    # завершить договор в проетке start
    @classmethod
    def check_name(cls, name):
        conn = sqlite3.connect('project.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все
        cur.execute('SELECT name FROM project')
        treats = cur.fetchall()  # сохраняем данные в переменную
        for el in treats:
            if name == el[0]:
                raise('Нельзя добавлять договора с одинаковым названием')
        cur.close()
        conn.close()

    @classmethod
    # возвращает id, имя, дата, активный договор и неактивные договора
    def take_all_for_inactive(cls):
        print('Выберите номер проекта, в котором хотите завершить договор')
        conn = sqlite3.connect('project.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все, где значение проектов NULL
        cur.execute('SELECT * FROM project WHERE treaty is not NULL')
        treats = cur.fetchall()  # сохраняем данные в переменную
        if treats != []:
            info = ''
            for el in treats:
                # выводим все проекты
                info += f'{el[0]}: [название проекта: {el[1]}, дата создания: {el[2]}, активный договор: {el[3]}, неактивные договоры: {"Пока нет ни одного неактивного договора" if el[4] == None else el[4]}]\n'
            cur.close()
            conn.close()
            return info
        raise ValueError('У вас нет ни одного с проекта с активным договором')

    @classmethod
    def active_to_inactive(cls, x):
        conn = sqlite3.connect('project.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все
        cur.execute(f'SELECT treaty FROM project WHERE id = {x}')
        value = cur.fetchall()[0][0]  # сохраняем значение
        cur.execute(f'SELECT inactive_treaty FROM project WHERE id = {x}')
        status = cur.fetchall()[0][0]  # сохраняем статус
        cur.execute(f'UPDATE project SET treaty = NULL WHERE id = {x}')
        if status is None:
            cur.execute(
                f'UPDATE project SET inactive_treaty="{value}" WHERE id = {x}')  # перезапись проектов
        else:
            cur.execute(
                f'UPDATE project SET inactive_treaty= inactive_treaty || ", {value}" WHERE id = {x}')  # перезапись проектов
        conn.commit()
        cur.close()
        conn.close()
        return value

    @classmethod
    def change_status_false_date_name(cls, name_p, name_t):
        conn = sqlite3.connect('project.sql')
        cur = conn.cursor()
        # обновляем статус по переданным параметрам
        cur.execute(
            f'SELECT inactive_treaty FROM project WHERE name = "{name_p}"')
        status = cur.fetchall()[0][0]
        cur.execute(
            f'UPDATE project SET treaty = NULL WHERE name = "{name_p}"')
        if status is None:
            cur.execute(
                f'UPDATE project SET inactive_treaty="{name_t}" WHERE name = "{name_p}"')  # перезапись проектов
        else:
            cur.execute(
                f'UPDATE project SET inactive_treaty= inactive_treaty || ", {name_t}" WHERE name = "{name_p}"')
        conn.commit()
        cur.close()
        conn.close()
        print('Статус успешно изменен ✅')

    # вызов всех функций start
    @classmethod
    def make_inactive_treaty(cls):
        print(cls.take_all_for_inactive())
        print('Введите 0, чтобы вернуться назад')
        num = int(input())
        if num == 0:
            return
        val = cls.active_to_inactive(num)
        Treaty.change_status_false_date_name(val)
    # вызов всех функций end

    # завершить договор в проетке end

    # добавить договор start

    @classmethod
    def take_id_name_status(cls):  # возвращает id, имя, дата, название договора
        print('''WARNING(В проект можно добавить только активный договор)
Выберите номер проекта, в который хотите добавить договор''')
        conn = sqlite3.connect('project.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все где проекты со значением NULL
        cur.execute('SELECT * FROM project WHERE treaty is NULL')
        treats = cur.fetchall()  # сохраняем данные в переменную
        if treats != []:
            info = ''
            for el in treats:
                # выводим все проекты
                info += f'{el[0]}: [название проекта: {el[1]}, дата создания: {el[2]}, активный договор: {"Неуказан"}, неактивные договоры: {"Пока нет ни одного неактивного договора" if el[4] == None else el[4]}]\n'
            cur.close()
            conn.close()
            return info
        raise ValueError('У вас нет ни одного свободного проекта')
    # добавить договор end

    # выбор проекта и договора start
    @classmethod
    def add_treaty_in_project(cls):
        print('Выберите номер проекта, в который хотите добавить проект')
        print(cls.take_id_name_status())
        print('Введите 0, чтобы вернуться назад')
        num_project = int(input())
        if num_project == 0:
            return
        print('Выберите id договора, который хотите добавить')
        print(Treaty.take_active())  # берем активные договоры
        num_treaty = int(input())
        Treaty.check_count(num_treaty)  # проверка количества строк в договорах
        cls.check_count(num_project)
        cls.add_treaty(num_treaty, num_project)
    # выбор проекта и договора end

    # проверяет количество строк в таблице и возвращает значение переданного числа start
    @classmethod
    def check_count(cls, x):
        conn = sqlite3.connect('project.sql')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM project;")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        if result != 0:
            if x in range(1, result+1):
                return
        raise ValueError('Такого числа нет в списке либо список пуст')
    # проверяет количество строк в таблице и возвращает значение переданного числа end

    # вызов всех функций start
    @classmethod
    def add_treaty(cls, id_treaty, id_project):
        project_name = cls.project_name(id_project)
        treaty_name = cls.treaty_name(id_treaty)
        cls.update_project(project_name, id_treaty)
        cls.insert_treaty(id_project, treaty_name)
        print('Данные успешно обновлены ✅')
    # вызов всех функций end

    # открываем бд с проектами и добавляем название договора start
    @classmethod
    def insert_treaty(cls, id, name_t):
        conn = sqlite3.connect('project.sql')
        cur = conn.cursor()
        # добавляем в таблицу название проекта по выбранным критериям
        cur.execute(f'UPDATE project SET treaty="{name_t}" WHERE id={id}')
        conn.commit()
        cur.close()
        conn.close()
    # открываем бд с проектами и добавляем название договора end

    # открываем бд с договорами и добавляем название проекта start
    @classmethod
    def update_project(cls, p_n, id_t):
        conn = sqlite3.connect('treaty.sql')
        cur = conn.cursor()
        # добавляем название проекта
        cur.execute(f'UPDATE treaty SET project="{p_n}" WHERE id={id_t}')
        conn.commit()
        cur.close()
        conn.close()
    # открываем бд с договорами и добавляем название проекта end

    # берем имя договора по переданным значениям start
    @classmethod
    def treaty_name(cls, id_treaty):
        conn = sqlite3.connect('treaty.sql')
        cur = conn.cursor()
        cur.execute(f'SELECT name FROM treaty WHERE id = {id_treaty};')
        name = cur.fetchall()[0][0]
        cur.close()
        conn.close()
        return name.strip()
    # берем имя договора по переданным значениям end

    # берем имя проекта по переданным значениям start
    @classmethod
    def project_name(cls, id_project):
        conn = sqlite3.connect('project.sql')
        cur = conn.cursor()
        cur.execute(f'SELECT name FROM project WHERE id = {id_project};')
        name = cur.fetchall()[0][0]
        cur.close()
        conn.close()
        return name.strip()
    # берем имя проекта по переданным значениям end

    # добавить договор end

    # проверка на корректность переданной строки start
    @classmethod
    def verify_name(cls, x):  # проверяет тип данных переданного значения
        if type(x) != str or len(x) > 50:
            print('Название должно быть строкой и иметь длину не больше 50 символов')
            raise TypeError(
                'Название должно быть строкой и иметь длину не больше 50 символов')

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, project):
        self.verify_name(project)
        self.__project = project
    # проверка на корректность переданной строки end

class Treaty:
    # класс для работы с договорами

    # создание бд start
    def __init__(self, treaty):
        self.treaty = treaty  # делаем проверку нашего значения
        conn = sqlite3.connect('treaty.sql')  # создаем бд
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS treaty (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50), date_today varchar(10), date_sign varchar(10), status BOOLEAN NULL, project varchar(50))')  # создаем таблицу
        self.check_name(treaty)
        cur.execute('INSERT INTO treaty (name, date_today) VALUES (?, ?)', (self.treaty,
                    date.today().strftime('%d.%m.%Y')))  # добавляем в таблицу название проекта
        conn.commit()  # подтверждаем нашу операцию
        cur.close()
        conn.close()  # закрываем таблицу
        print('Договор успешно создан ✅')
    # создание бд end

    # возвращение списков договоров start
    @classmethod
    def check_name(cls, name):
        conn = sqlite3.connect('treaty.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все
        cur.execute('SELECT name FROM treaty')
        treats = cur.fetchall()  # сохраняем данные в переменную
        if treats != []:
            for el in treats:
                if name == el[0]:
                    raise('Нельзя добавлять договора с одинаковым названием')
        cur.close()
        conn.close()
    
    @classmethod
    def take_id_name_status(cls):  # возвращает id имя и статус договора
        conn = sqlite3.connect('treaty.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все
        cur.execute('SELECT * FROM treaty WHERE status = "True"')
        treats = cur.fetchall()  # сохраняем данные в переменную
        if treats != []:
            info = ''
            for el in treats:
                # выводим все договоры
                info += f'{el[0]} [название договора: {el[1]}, дата создания: {el[2]} дата подписания: {"Неподписан" if el[3] is None else el[3]}, статус: {"Неуказан" if el[4]==None else "Активен" if el[4]=="True" else "Завершен"}, проект: {"Неуказан" if el[5]==None else el[5]}]\n'
            cur.close()
            conn.close()
            return info  # возвращаем список
        raise ValueError('Нет активных договоров')

    @classmethod
    def take_id_name_status_flase(cls):  # возвращает id имя и статус договора
        conn = sqlite3.connect('treaty.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все
        cur.execute('SELECT * FROM treaty WHERE status is NULL')
        treats = cur.fetchall()  # сохраняем данные в переменную
        if treats != []:
            info = ''
            for el in treats:
                # выводим все договоры
                info += f'{el[0]} [название договора: {el[1]}, дата создания: {el[2]} дата подписания: {"Неподписан" if el[3] is None else el[3]}, статус: {"Неуказан" if el[4]==None else "Активен" if el[4]=="True" else "Завершен"}, проект: {"Неуказан" if el[5]==None else el[5]}]\n'
            cur.close()
            conn.close()
            return info
        raise ValueError('Нет активных договоров')

    @classmethod
    def take_active(cls):  # возвращает список договоров, которые активны и не имеют договора
        conn = sqlite3.connect('treaty.sql')  # подключаем бд
        cur = conn.cursor()
        # выбираем все, гда статус True и нет проекта
        cur.execute(
            f'SELECT * FROM treaty WHERE status = "True" and project is NULL')
        treats = cur.fetchall()  # сохраняем данные в переменную
        if treats!= []:
            info = ''
            for el in treats:
                info += f'{el[0]}: [название договора: {el[1]}, дата создания: {el[2]}, дата подписания: {"Неподписан" if el[3] is None else el[3]}, статус: {"Неуказан" if el[4]==None else "Активен" if el[4]=="True" else "Завершен"}, проект: {"Неуказан"}]\n'  # выводим все договоры
            cur.close()
            conn.close()
            return info
        raise ValueError('Нет активных договоров')
    # возвращение списков договоров end

    # изменят статус договора на True start

    @classmethod
    def change_status_true_date(cls, num):
        cls.check_count(num)  # проверяем наличие id в таблице
        conn = sqlite3.connect('treaty.sql')
        cur = conn.cursor()
        # выбираем все по условиям id
        cur.execute(f'SELECT date_sign FROM treaty WHERE id={num}')
        data = cur.fetchall()[0][0]  # сохраняем наше значение
        if data == None:
            # обновляем статус
            cur.execute(
                f'UPDATE treaty SET status="{True}", date_sign="{date.today().strftime("%d.%m.%Y")}" WHERE id={num}')
        else:
            raise ValueError('Вы уже подтвердили этот договор')
        conn.commit()  # подтверждаем нашу операцию
        cur.close()
        conn.close()
        print('Статус успешно изменен ✅')
    # изменят статус договора на True end

    # изменят статус договора на False start

    @classmethod
    def change_status_false_date(cls, num):
        cls.check_count(num)
        conn = sqlite3.connect('treaty.sql')  # подключаем бд
        cur = conn.cursor()
        # обновляем статус по переданным параметрам
        cur.execute(f'UPDATE treaty SET status="{False}" WHERE id={num}')
        conn.commit()
        cur.close()
        conn.close()
        print('Статус успешно изменен ✅')

    # меняем статус для проекта и для договора start
    @classmethod
    def change_status_false_project(cls, num):
        cls.check_count(num)
        conn = sqlite3.connect('treaty.sql')  # подключаем бд
        cur = conn.cursor()
        cur.execute(f'SELECT project FROM treaty WHERE id={num}')
        name_p = cur.fetchall()[0][0]
        cur.execute(f'SELECT name FROM treaty WHERE id={num}')
        name_t = cur.fetchall()[0][0]
        if name_p == None:
            # обновляем статус по переданным параметрам
            cur.execute(f'UPDATE treaty SET status="{False}" WHERE id={num}')
            conn.commit()
            cur.close()
            conn.close()
        else:
            Project.change_status_false_date_name(name_p, name_t)
            cur.execute(f'UPDATE treaty SET status="{False}" WHERE id={num}')
            conn.commit()
            cur.close()
            conn.close()
        # меняем статус для проекта и для договора end

    @classmethod
    def change_status_false_date_name(cls, name):
        conn = sqlite3.connect('treaty.sql')
        cur = conn.cursor()
        # обновляем статус по переданным параметрам
        cur.execute(f'UPDATE treaty SET status="{False}" WHERE name="{name}"')
        conn.commit()
        cur.close()
        conn.close()
        print('Статус успешно изменен ✅')

    # вызов всех функций start
    @classmethod
    def finish_treaty(cls):
        print('Выберите номер договра, который хотите завершить')
        print(Treaty.take_id_name_status())
        print('Введите 0, чтобы вернуться назад')
        num = int(input())
        if num == 0:
            return
        Treaty.change_status_false_project(num)
    # вызов всех функций end

    # изменят статус договора на False end

    # проверяет количество строк в таблице и возвращает значение переданного числа start

    @classmethod
    def check_count(cls, x):
        conn = sqlite3.connect('treaty.sql')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM treaty")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        if result != 0:
            if x in range(1, result+1):
                return
        raise ValueError('Такого числа нет в списке либо список пуст')
    # проверяет количество строк в таблице и возвращает значение переданного числа end

    @classmethod
    def confirm_treaty(cls):
        print('Выберите номер договра, который хотите подтвердить. Обратите внимание - нельзя активировать завершенный договор')
        print(Treaty.take_id_name_status_flase())
        print('Введите 0, чтобы вернуться назад')
        action = input()
        if int(action) == 0:
            return
        Treaty.change_status_true_date(int(action))

    # проверяем переданную строку start
    @classmethod
    def verify_name(cls, x):
        if type(x) != str or len(x) > 50:
            print('Название должно быть строкой и иметь длину не больше 50 символов')
            raise TypeError(
                'Название должно быть строкой и иметь длину не больше 50 символов')

    @property
    def treaty(self):
        return self.__treaty.strip()

    @treaty.setter
    def treaty(self, treaty):
        self.verify_name(treaty)
        self.__treaty = treaty
    # проверяем переданную строку end    