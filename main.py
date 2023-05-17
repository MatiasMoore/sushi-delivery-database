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
        "2 - пользователи\n"
        "3 - заказы\n"
        "4 - доставщики\n"
        "5 - сушисты\n", 1, 5)
    if userChoice == -1:
        return -1
    res = int(0)
    if userChoice == 1:
        res = genericCRUD(dbConnection, 
        ["блюда", "новое блюдо", "блюдо"], 
        "dishes", "id_dish", 
        [ ["name", ""], ["price", ""] ])
    elif userChoice == 2:
        res = genericCRUD(dbConnection, 
        ["пользователей", "нового пользователя", "пользователя"], 
        "clients", "id_client", 
        [ ["name", ""], ["phone_number", ""], ["address", ""]])
    elif userChoice == 3:
        res = ordersCRUD(dbConnection)
    elif userChoice == 4:
        res = genericCRUD(dbConnection, 
        ["доставщиков", "нового доставщика", "доставщика"], 
        "deliverymen", "id_deliveryman", 
        [ ["name", ""], ["surname", ""], ["salary", ""]])
    elif userChoice == 5:
        res = genericCRUD(dbConnection, 
        ["сушистов", "нового сушиста", "сушиста"], 
        "chefs", "id_chef", 
        [ ["name", ""], ["surname", ""], ["salary", ""]])
        
    return res

def newOrderDialog(dbConnection: MySQLConnection, table, idName, params, existingId=None):
    for pair in params:
        pair[1] = input(f"Введите значения для столбца { pair[0] }\n")
        
    createdId = existingId
    if existingId == None:
        sq.addOne(dbConnection, table, params)
        createdId = sq.getLastId(dbConnection)
    else:
        sq.updateOne(dbConnection, table, idName, existingId, params)
    
    addDishes = askUser(
        "Хотите добавить блюда в заказ?\n"
        "1 - да\n"
        "2 - нет\n", 1, 2
    )
    if addDishes != 2 and addDishes != -1:
        sq.getAll(dbConnection, "dishes")
        sum = int(0)
        while True:
            dishToAdd = input(
                "Введите id блюда для добавления в заказ\n"
                "enter - завершить добавление блюд\n", 
            )
            try:
                dishToAdd = int(dishToAdd)
            except:
                sq.updateOne(dbConnection, table, idName, createdId, [["sum",f"{sum}"]])
                break
            getRes = sq.getOne(dbConnection, "dishes", "id_dish", dishToAdd)
            if getRes == -1:
                print("Блюда с таким id не существует\n")
                continue
            info = sq.getOneInfo(dbConnection, "dishes", "id_dish", dishToAdd)
            price = int(info[2])
            sum += price
            sq.addOne(dbConnection, "orders_to_dishes", [["id_order", f"{ createdId }"], ["id_dish", f"{ dishToAdd }"]])
    
    addPromo = askUser(
        "Хотите добавить промокод в заказ?\n"
        "1 - да\n"
        "2 - нет\n", 1, 2
    )
    if addPromo != 2 and addPromo != -1:    
        sq.getAll(dbConnection, "special_offers")
        while True:
            promoToAdd = input(
                "Введите id промокода для добавления в заказ\n"
            )
            try:
                promoToAdd = int(promoToAdd)
            except:
                print("Неверное значение, попробуйте снова")
                continue
            getRes = sq.getOne(dbConnection, "special_offers", "id_special_offer", promoToAdd)
            if getRes == -1:
                print("Промокода с таким id не существует, попробуйте снова")
                continue
            sq.updateOne(dbConnection, table, idName, createdId, [["id_special_offer", f"{ promoToAdd }"]])
            break
    else:
        sq.setNullParams(dbConnection, table, idName, createdId, ["id_special_offer"])
    sq.printAllOrdersWithDishes(dbConnection, createdId)
    print("Созданная запись")

def ordersCRUD(dbConnection: MySQLConnection):
    option = askUser(
        "1 - просмотреть заказы\n"
        "2 - создать новый заказ\n"
        "3 - изменить заказ\n"
        "4 - удалить заказ\n", 1, 4)
    if option == -1:
        return -1
    
    table = "orders"
    idName = "id_order"
    params = [ ["date", ""], ["time", ""], ["address", ""]]
    
    res = 0
    
    if option == 1:
        sq.printAllOrdersWithDishes(dbConnection)
    elif option == 2:
        res = newOrderDialog(dbConnection, table, idName, params) 
    elif option == 3:
        id = input("Введите id записи для редактирования\n")
        getRes = sq.getOne(dbConnection, table, idName, id, print=False)
        if getRes == -1:
            print("Записи с таким id не существует\n")
            return -1
        sq.printAllOrdersWithDishes(dbConnection, id)
        confirm = askUser(
            "Эта запись будет изменена\n"
            "1 - изменить\n"
            "2 - отмена\n", 1, 2)
        if confirm == 2 or confirm == -1:
            return -1
        sq.deleteOne(dbConnection, "orders_to_dishes", "id_order", id)
        res = newOrderDialog(dbConnection, table, idName, params, id)
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
    
    return res

def genericCRUD(dbConnection: MySQLConnection, nameList, table, idName, params):
    option = askUser(
        f"1 - просмотреть {nameList[0]}\n"
        f"2 - создать {nameList[1]}\n"
        f"3 - изменить {nameList[2]}\n"
        f"4 - удалить {nameList[2]}\n", 1, 4)
    if option == -1:
        return -1
        
    if option == 1:
        sq.getAll(dbConnection, table)
    elif option == 2:
        for pair in params:
            pair[1] = input(f"Введите значения для столбца { pair[0] }\n")
        sq.addOne(dbConnection, table, params)
        sq.getOne(dbConnection, table, idName, sq.getLastId(dbConnection))
        print("Созданная запись")
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
        sq.getOne(dbConnection, table, idName, id)
        print("Созданная запись")
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
        print("Запись удалена")
    
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