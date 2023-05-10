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
    
def getAll(connection: MySQLConnection, table: str):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM { table }}")
    
    printAsTable(cursor)

    cursor.close()
    
def getOne(connection: MySQLConnection, table: str, idName: str, id: int):
    res = bool()
    cursor = connection.cursor()
    queryStr = f"SELECT * FROM { table } WHERE { table }.{ idName } = { id }"
    cursor.execute(queryStr)
    if cursor.fetchall().__len__() != 0:
        cursor.execute(queryStr)
        printAsTable(cursor)
        res = 0
    else:
        res = -1

    cursor.close()
    return res

def addOne(connection: MySQLConnection, table: str, paramNames, paramValues):
    cursor = connection.cursor()
    columnsStr = ""
    for name in paramNames:
        columnsStr += f"{ name }, "
    valuesStr = ""
    for value in paramValues:
        valuesStr += f"{ value }, "
    cursor.execute(f"INSERT INTO {table}({ columnsStr[0: -2] }) VALUES ({ valuesStr[0: -2] })")
    connection.commit()
    cursor.close()

def updateOne(connection: MySQLConnection, table: str, idName: str, id: int, paramNames, paramValues):
    cursor = connection.cursor()
    paramsStr = ""
    for name, value in zip(paramNames, paramValues):
        paramsStr += f"{ name } = { value }, "
    
    queryStr = f"UPDATE { table } SET { paramsStr[0: -2] } WHERE { table }.{ idName } = { id }"
    cursor.execute(queryStr)
    connection.commit()
    cursor.close()

def deleteOne(connection: MySQLConnection, table: str, idName: str, id: int):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM { table } WHERE { table }.{ idName } = { id }")
    connection.commit()
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
    cursor.execute(f"UPDATE dishes SET name = \"{ newName }\", price = { newPrice } WHERE dishes.id_dish = { idDish }")
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