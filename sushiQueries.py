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
def printAsTable(cursor: MySQLCursor, maxWidths=None):
    field_names = [i[0] for i in cursor.description] 
    table = cursor.fetchall()
    for i, row in enumerate(table):
        newRow = []
        for elem in row:
            if elem == None:
                newRow.append("NULL")
            else:
                newRow.append(elem)
        table[i] = newRow
    print(tabulate(table, headers=field_names, tablefmt='psql', maxcolwidths=maxWidths))

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
    
def printAllOrdersWithDishes(connection: MySQLConnection, oneId=None):
    cursor = connection.cursor()
    
    extra = ""
    if (oneId != None):
        extra = f"WHERE orders.id_order = { oneId }"
    
    cursor.execute(f"SELECT orders.id_order, orders.date, orders.time, orders.sum, orders.address, special_offers.promocode, GROUP_CONCAT(dishes.name) AS dishes_list " "from orders " 
    "left join special_offers on special_offers.id_special_offer = orders.id_special_offer "
    "left join orders_to_dishes on orders_to_dishes.id_order = orders.id_order "
    f"left join dishes on dishes.id_dish = orders_to_dishes.id_dish {extra} GROUP BY orders.id_order ORDER BY orders.id_order")
    
    printAsTable(cursor, [None]*6 + [80])

    cursor.close()
    
def getLastId(connection: MySQLConnection):
    cursor = connection.cursor()
    cursor.execute("SELECT LAST_INSERT_ID()")
    id = int(cursor.fetchall()[0][0])
    cursor.close()
    return id
    
def getAll(connection: MySQLConnection, table: str):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM { table }")
    
    printAsTable(cursor)

    cursor.close()

def getOneInfo(connection: MySQLConnection, table: str, idName: str, id: int):
    cursor = connection.cursor()
    queryStr = f"SELECT * FROM { table } WHERE { table }.{ idName } = { id }"
    cursor.execute(queryStr)
    info = cursor.fetchall()[0]
    cursor.close()
    return info
    
def getOne(connection: MySQLConnection, table: str, idName: str, id: int, print=True):
    res = bool()
    cursor = connection.cursor()
    queryStr = f"SELECT * FROM { table } WHERE { table }.{ idName } = { id }"
    cursor.execute(queryStr)
    if cursor.fetchall().__len__() != 0:
        cursor.execute(queryStr)
        if print:
            printAsTable(cursor)
        else:
            cursor.fetchall()
        res = 0
    else:
        res = -1

    cursor.close()
    return res

def addOne(connection: MySQLConnection, table: str, params):
    cursor = connection.cursor()
    columnsStr = ""
    valuesStr = ""
    for pair in params:
        columnsStr += f"{ pair[0] }, "
        valuesStr += f"\"{ pair[1] }\", "
    cursor.execute(f"INSERT INTO {table}({ columnsStr[0: -2] }) VALUES ({ valuesStr[0: -2] })")
    connection.commit()
    cursor.close()

def setNullParams(connection: MySQLConnection, table: str, idName: str, id: int, params):
    cursor = connection.cursor()
    paramsStr = ""
    for param in params:
        paramsStr += f"{ param } = NULL, "
    
    queryStr = f"UPDATE { table } SET { paramsStr[0: -2] } WHERE { table }.{ idName } = { id }"
    cursor.execute(queryStr)
    connection.commit()
    cursor.close()
    
def updateOne(connection: MySQLConnection, table: str, idName: str, id: int, params):
    cursor = connection.cursor()
    paramsStr = ""
    for pair in params:
        paramsStr += f"{ pair[0] } = \"{ pair[1] }\", "
    
    queryStr = f"UPDATE { table } SET { paramsStr[0: -2] } WHERE { table }.{ idName } = { id }"
    cursor.execute(queryStr)
    connection.commit()
    cursor.close()

def deleteOne(connection: MySQLConnection, table: str, idName: str, id: int):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM { table } WHERE { table }.{ idName } = { id }")
    connection.commit()
    cursor.close()  