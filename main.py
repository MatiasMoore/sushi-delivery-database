import sushiQueries as sq
from sushiQueries import MySQLConnection
def askUser(message: str, minPossible: int, maxPossible: int):
    choice = input(message)
    try:
        choice = int(choice)
    except:
        print("Ошибка ввода")
        return -1
    if choice < minPossible or choice > maxPossible:
        print("Выбран недействительный вариант")
        return -1
    return choice
        
    
def analyticsDialog(dbConnection: MySQLConnection):
    userChoice = askUser(
        "Выберите режим работы\n"
        "1 - просмотреть заказы за промежуток времени\n"
        "2 - найти доставщиков по полному имени\n", 1, 2)
    if userChoice == -1:
        return -1
    
    if userChoice == 1:
        print("Ввод даты в формате ГГГГ-ММ-ДД")
        dateA = input("Введите начальную дату\n")
        dateb = input("Введите конечную дату\n")
        sq.getOrdersInTimePeriod(dbConnection, dateA, dateb)
    elif userChoice == 2:
        name = input("Введите имя доставщика\n")
        surname = input("Введите фамилию доставщика\n")
        sq.getDeliveyManByFullName(dbConnection, name, surname)
    
    return 0

def crudsDialog(dbConnection: MySQLConnection):
    userChoice = askUser(
        "Выберите таблицу\n"
        "1 - блюда\n"
        "2 - пользователи\n", 1, 2)
    if userChoice == -1:
        return -1
    res = int(0)
    if userChoice == 1:
        res = dishesCRUD(dbConnection)
    elif userChoice == 2:
        res = clientsCRUD(dbConnection)
        
    return res

def dishesCRUD(dbConnection: MySQLConnection):
    option = askUser(
        "1 - просмотреть блюда\n"
        "2 - создать новое блюдо\n"
        "3 - изменить блюдо\n"
        "4 - удалить блюдо\n", 1, 4)
    if option == -1:
        return -1
    
    table = "dishes"
    idName = "id_dish"
    params = [ ["name", ""], ["price", ""]]
    
    if option == 1:
        sq.getAll(dbConnection, table)
    elif option == 2:
        for pair in params:
            pair[1] = input(f"Введите значения для столбца { pair[0] }\n")
        sq.addOne(dbConnection, table, params)
    elif option == 3:
        id = input("Введите id записи для редактирования\n")
        getRes = sq.getOne(dbConnection, table, idName, id)
        if getRes == -1:
            print("Записи с таким id не существует\n")
            return -1
        confirm = askUser(
            "Эта запись будет изменена\n"
            "1 - изменить\n"
            "2 - отмена\n", 1, 2)
        if confirm == 2 or confirm == -1:
            return -1
        for pair in params:
            pair[1] = input(f"Введите новое значения для столбца { pair[0] }\n")
        sq.updateOne(dbConnection, table, idName, id, params)
    elif option == 4:
        id = input("Введите id записи для удаления\n")
        getRes = sq.getOne(dbConnection, table, idName, id)
        if getRes == -1:
            print("Записи с таким id не существует\n")
            return -1
        confirm = askUser(
            "Эта запись будет удалена\n"
            "1 - удалить\n"
            "2 - отмена\n", 1, 2)
        if confirm == 2 or confirm == -1:
            return -1
        sq.deleteOne(dbConnection, table, idName, id)
    
    return 0

def clientsCRUD(dbConnection: MySQLConnection):
    option = askUser(
        "1 - просмотреть клиентов\n"
        "2 - создать нового клиента\n"
        "3 - изменить клиента\n"
        "4 - удалить клиента\n", 1, 4)
    if option == -1:
        return -1
    
    table = "clients"
    idName = "id_client"
    params = [ ["name", ""], ["phone_number", ""], ["address", ""]]
    
    if option == 1:
        sq.getAll(dbConnection, table)
    elif option == 2:
        for pair in params:
            pair[1] = input(f"Введите значения для столбца { pair[0] }\n")
        sq.addOne(dbConnection, table, params)
    elif option == 3:
        id = input("Введите id записи для редактирования\n")
        getRes = sq.getOne(dbConnection, table, idName, id)
        if getRes == -1:
            print("Записи с таким id не существует\n")
            return -1
        confirm = askUser(
            "Эта запись будет изменена\n"
            "1 - изменить\n"
            "2 - отмена\n", 1, 2)
        if confirm == 2 or confirm == -1:
            return -1
        for pair in params:
            pair[1] = input(f"Введите новое значения для столбца { pair[0] }\n")
        sq.updateOne(dbConnection, table, idName, id, params)
    elif option == 4:
        id = input("Введите id записи для удаления\n")
        getRes = sq.getOne(dbConnection, table, idName, id)
        if getRes == -1:
            print("Записи с таким id не существует\n")
            return -1
        confirm = askUser(
            "Эта запись будет удалена\n"
            "1 - удалить\n"
            "2 - отмена\n", 1, 2)
        if confirm == 2 or confirm == -1:
            return -1
        sq.deleteOne(dbConnection, table, idName, id)
    
    return 0

if __name__ == '__main__':
    # Подключится к БД
    try:
        dbConnection = sq.create_connection("localhost", "root", "Np3nqeet", "sushi_delivery")
        print("\nSuccessfuly connected to DB\n")
    except sq.Error:
        print(f"\nThe error occurred: '{sq.Error}'\n")
        quit()
        
    # Основной цикл программы
    while True:
        menuChoice = askUser(
           "Выберите тип операций\n"
           "1 - аналитические запросы\n"
           "2 - CRUD запросы\n" 
           "3 - завершить работу\n", 1, 3)
        if menuChoice == 3:
            break
        res = int()
        if menuChoice == 1:
            res = analyticsDialog(dbConnection)
        elif menuChoice == 2:
            res = crudsDialog(dbConnection)
        input("Нажмите enter для продолжения\n")

    dbConnection.close()