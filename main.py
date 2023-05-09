import mysql.connector
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor
import datetime
from tabulate import tabulate

# Инициализировать БД
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    return connection

# Печать красивой таблицы в консоль
def printAsTable(cursor: MySQLCursor):
    field_names = [i[0] for i in cursor.description] 
    print(tabulate(cursor.fetchall(), headers=field_names, tablefmt='psql'))

# Получить заказы за промежуток времени и вывести в консоль
def getOrdersInTimePeriod(connection: MySQLConnection, startDate: str, endDate: str):
    cursor = connection.cursor()
    cursor.execute(f"CALL GetOrdersInDateRange(\"{ startDate }\", \"{ endDate }\")")
    
    printAsTable(cursor)

    cursor.close()
    
# Получить доставщика по полному имени и вывести в консоль
def getDeliveyManByFullName(connection: MySQLConnection, targetName: str, targetSurname: str):
    cursor = connection.cursor()
    cursor.execute(f"CALL GetDeliverymenByFullName(\"{ targetName }\", \"{ targetSurname }\")")
    
    printAsTable(cursor)

    cursor.close()
    
# Получить все блюда и вывести в консоль
def getAllDishes(connection: MySQLConnection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dishes")
    
    printAsTable(cursor)

    cursor.close()
    
    
# Получить одно блюдо по id и вывести в консоль
def getDish(connection: MySQLConnection, idDish: int):
    res = bool()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM dishes WHERE dishes.id_dish = { idDish }")
    if cursor.fetchall().__len__() != 0:
        cursor.execute(f"SELECT * FROM dishes WHERE dishes.id_dish = { idDish }")
        printAsTable(cursor)
        res = 1
    else:
        res = 0

    cursor.close()
    return res

# Добавить новое блюдо
def addNewDish(connection: MySQLConnection, name: str, price: int):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO dishes(name, price) VALUES (\"{ name }\", {price})")
    connection.commit()
    cursor.close()

# Изменить существующее блюдо
def updateDish(connection: MySQLConnection, idDish: int, newName: str, newPrice: int):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE dishes SET name = \"{ name }\", price = {price} WHERE dishes.id_dish = { idDish }")
    connection.commit()
    cursor.close()

# Удалить существующее блюдо
def deleteDish(connection: MySQLConnection, idDish: int):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM dishes WHERE dishes.id_dish = { idDish }")
    connection.commit()
    cursor.close()  
    
# Получить всех клиентов и вывести в консоль
def getAllClients(connection: MySQLConnection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients")
    
    printAsTable(cursor)

    cursor.close()
    
    
# Получить одного клиента и вывести в консоль
def getClient(connection: MySQLConnection, idClient: int):
    res = bool()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM clients WHERE clients.id_client = { idClient }")
    if cursor.fetchall().__len__() != 0:
        cursor.execute(f"SELECT * FROM clients WHERE clients.id_client = { idClient }")
        printAsTable(cursor)
        res = 1
    else:
        res = 0

    cursor.close()
    return res

# Добавить нового клиента
def addNewClient(connection: MySQLConnection, name: str, phoneNumber: str, address: str):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO clients(name, phone_number, address) VALUES (\"{ name }\", \"{ phoneNumber }\", \"{ address }\")")
    connection.commit()
    cursor.close()
 
# Изменить существующего клиента
def updateClient(connection: MySQLConnection, idClient: int, newName: str, newPhoneNumber: str, newAddress: str):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE clients SET name = \"{ newName }\", phone_number = \"{ newPhoneNumber }\", address = \"{ newAddress }\" WHERE clients.id_client = { idClient }")
    connection.commit()
    cursor.close()

# Удалить существующего клиента
def deleteClient(connection: MySQLConnection, idClient: int):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM clients WHERE clients.id_client = { idClient }")
    connection.commit()
    cursor.close()  
    
if __name__ == '__main__':
    # Подключится к БД
    try:
        dbConnection = create_connection("localhost", "root", "Np3nqeet", "sushi_delivery")
        print("\nSuccessfuly connected to DB\n")
    except Error:
        print(f"\nThe error occurred: '{Error}'\n")
        quit()
    # Основной цикл программы
    while True:
        # Переподключится при надобности
        if (not dbConnection.is_connected()):
            dbConnection.reconnect()
        try:
            # Получение ввода пользователя
            userChoice = int(input(
                "Выберите режим работы\n"
                "1 - просмотреть заказы за промежуток времени\n"
                "2 - найти доставщиков по полному имени\n"
                "3 - просмотреть все блюда\n"
                "4 - добавить новое блюдо\n"
                "5 - изменить блюдо\n"
                "6 - удалить блюдо\n"
                "7 - просмотреть всех пользователей\n"
                "8 - добавить нового пользователя\n"
                "9 - изменить пользователя\n"
                "10 - удалить пользователя\n"
                "Enter - завершить работу\n"
            ))
            
            if (userChoice == 1):
                print("Ввод даты в формате ГГГГ-ММ-ДД")
                dateA = input("Введите начальную дату\n")
                dateb = input("Введите конечную дату\n")
                getOrdersInTimePeriod(dbConnection, dateA, dateb)
            elif (userChoice == 2):
                name = input("Введите имя доставщика\n")
                surname = input("Введите фамилию доставщика\n")
                getDeliveyManByFullName(dbConnection, name, surname)
            elif (userChoice == 3):
                getAllDishes(dbConnection)
            elif (userChoice == 4):
                name = input("Введите имя блюда\n")
                price = int(input("Введите цену блюда\n"))
                addNewDish(dbConnection, name, price)
            elif (userChoice == 5):
                id = int(input("Введите id блюда\n"))
                name = input("Введите новое имя блюда\n")
                price = int(input("Введите новую цену блюда\n"))
                updateDish(dbConnection, id, name, price)
            elif (userChoice == 6):
                id = int(input("Введите id для удаления\n"))
                found = getDish(dbConnection, id)
                if not found:
                    print("Такой записи не существует")
                else:
                    finalCheck = int(input(
                        "Эта запись будет удалена\n"
                        "1 - удалить\n"
                        "2 - отмена\n"
                        ))
                    if (finalCheck == 1):
                        dbConnection.reconnect()
                        deleteDish(dbConnection, id)
            elif (userChoice == 7):
                getAllClients(dbConnection)
            elif (userChoice == 8):
                name = input("Введите имя пользователя\n")
                phoneNumber = input("Введите номер телефона\n")
                addr = input("Введите адрес\n")
                addNewClient(dbConnection, name, phoneNumber, addr)
            elif (userChoice == 9):
                id = int(input("Введите id пользователя\n"))
                name = input("Введите новое имя пользователя\n")
                phoneNumber = input("Введите новый номер телефона\n")
                addr = input("Введите новый адрес\n")
                updateClient(dbConnection, id, name, phoneNumber, addr)
            elif (userChoice == 10):
                id = int(input("Введите id для удаления\n"))
                found = getClient(dbConnection, id)
                if not found:
                    print("Такой записи не существует")
                else:
                    finalCheck = int(input(
                        "Эта запись будет удалена\n"
                        "1 - удалить\n"
                        "2 - отмена\n"
                        ))
                    if (finalCheck == 1):
                        dbConnection.reconnect()
                        deleteClient(dbConnection, id)
            else:
                print("Выбран недействительный режим работы!")
                break
        except:
            print("Завершение работы")
            break

        input("Нажмите enter для продолжения\n")

    dbConnection.close()