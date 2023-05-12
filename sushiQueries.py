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
    cursor.execute(f"SELECT * FROM { table }")
    
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

def addOne(connection: MySQLConnection, table: str, params):
    cursor = connection.cursor()
    columnsStr = ""
    valuesStr = ""
    for pair in params:
        columnsStr += f"{ pair[0] }, "
        valuesStr += f"{ pair[1] }, "
    print(f"INSERT INTO {table}({ columnsStr[0: -2] }) VALUES ({ valuesStr[0: -2] })")
    # cursor.execute(f"INSERT INTO {table}({ columnsStr[0: -2] }) VALUES ({ valuesStr[0: -2] })")
    # connection.commit()
    cursor.close()

def updateOne(connection: MySQLConnection, table: str, idName: str, id: int, params):
    cursor = connection.cursor()
    paramsStr = ""
    for pair in params:
        paramsStr += f"{ pair[0] } = { pair[1] }, "
    
    queryStr = f"UPDATE { table } SET { paramsStr[0: -2] } WHERE { table }.{ idName } = { id }"
    print(queryStr)
    # cursor.execute(queryStr)
    # connection.commit()
    cursor.close()

def deleteOne(connection: MySQLConnection, table: str, idName: str, id: int):
    cursor = connection.cursor()
    print(f"DELETE FROM { table } WHERE { table }.{ idName } = { id }")
    # cursor.execute(f"DELETE FROM { table } WHERE { table }.{ idName } = { id }")
    # connection.commit()
    cursor.close()  