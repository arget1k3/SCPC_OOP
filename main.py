from project_treaty import Project, Treaty
from menu import Menu

# работа нашей проги start
while True:
    m = Menu()
    m.main_menu()  # печатаем главное меню
    item = m.check_num(input())
    if item == 1:  # работа с проектами
        try:
            Treaty.check_count(1)  # проверяем наше число
            while True:
                m.project_menu()
                res = m.check_num(input())
                if res == 1:  # создаем проект
                    try:
                        n_d = m.create_project_menu()
                        Project(n_d)
                    except:
                        print('Нельзя добавлять проекты с одинаковым названием и название не должно превышать 50 символов')
                elif res == 2:  # добавляем договор к проекту
                    try:
                        Project.add_treaty_in_project()
                    except:
                        print('Упс, кажется что-то пошло не так! Возможно у вас нет свободных проектов, либо у вас нет ни одного активного договора')
                elif res == 3:  # завершаем договор
                    try:
                        Project.make_inactive_treaty()
                    except:
                        print(
                            'Упс, кажется что-то пошло не так! Проверьте корректность введенных данных, возможно у вас нет ни одного проекта с активным договором')
                elif res == 9:  # просмотр всех договоров и проектов
                    try:
                        m.project_treaty()
                    except:
                        print('Список пуст')    
                elif res == 4:  # выход в главное меню
                    break
                if res not in (1,2,3,9,4):
                    print('Введите число из представленного списка')
        except:
            print('Вы не можете создать проект, пока у вас нет ни одного созданного договора')
    elif item == 2:  # работа с договорами
        while True:
            m.treaty_menu()
            res = m.check_num(input())
            if res == 1:  # создаем договор
                try:
                    n_d = m.create_treaty_menu()
                    Treaty(n_d)
                except:
                    print('Нельзя добавлять договора с одинаковым названием и название не должно превышать 50 символов')
            elif res == 2:  # подтверждаем договор
                try:
                    Treaty.confirm_treaty()
                except:
                    print('Упс, кажется что-то пошло не так! Проверьте корректность введенных данных, возможно вы уже подтвердили этот договор или этого договора нет в списке.')
            elif res == 3:  # завершаем договор
                try:
                    Treaty.finish_treaty()
                except:
                    print('Упс, кажется что-то пошло не так! Проверьте корректность введенных данных, возможно вы еще не добавили ни одного договора или ввели некорректный номер договора.')
            elif res == 9:  # просмотр всех договоров и проектов
                try:
                    m.project_treaty()
                except:
                    print('Список пуст')    
            elif res == 4:  # выход в главное меню
                break
            if res not in (1,2,3,9,4):
                print('Введите число из представленного списка')
    elif item == 9:  # просмотр всех договоров и проектов
            try:
                m.project_treaty()
            except:
                print('Список пуст')    
    elif item == 4:  # завершение программы
        print('До встречи 😃')
        break
    if item not in (1,2,9,4):
        print('Введите число из представленного списка')
# работа нашей проги end
