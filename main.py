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
        
    
def analyticsDialog():
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

def crudsDialog():
    userChoice = askUser(
        "Выберите таблицу\n"
        "1 - блюда\n"
        "2 - пользователи\n", 1, 2)
    if userChoice == -1:
        return -1
    if userChoice == 1:
        ...
    elif userChoice == 2:
        ...
        
    return 0

def CRUDDialog(connection: MySQLConnection, tableName: str):
    option = askUser(
        "1 - просмотреть записи\n"
        "2 - создать запись\n"
        "3 - изменить запись\n"
        "4 - удалить запись\n", 1, 4)
    if option == -1:
        return -1
    
    if option == 1:
        sq.getAll(connection, tableName)
    elif option == 2:
        ...
    elif option == 3:
        ...
    elif option == 4:
        ...
    return 0

def dishesCRUD():
    ...

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
           "2 - CRUD запросы\n", 1, 2
           )
        if menuChoice == -1:
            break
        res = int()
        if menuChoice == 1:
            res = analyticsDialog()
        elif menuChoice == 2:
            res = crudsDialog()
        if res == -1:
            break

    dbConnection.close()