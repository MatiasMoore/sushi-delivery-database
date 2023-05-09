import sushiQueries as sq
    
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
                sq.getOrdersInTimePeriod(dbConnection, dateA, dateb)
            elif (userChoice == 2):
                name = input("Введите имя доставщика\n")
                surname = input("Введите фамилию доставщика\n")
                sq.getDeliveyManByFullName(dbConnection, name, surname)
            elif (userChoice == 3):
                sq.getAllDishes(dbConnection)
            elif (userChoice == 4):
                name = input("Введите имя блюда\n")
                price = int(input("Введите цену блюда\n"))
                sq.addNewDish(dbConnection, name, price)
            elif (userChoice == 5):
                id = int(input("Введите id блюда\n"))
                found = sq.getDish(dbConnection, id)
                if not found:
                    print("Такой записи не существует")
                else:
                    finalCheck = int(input(
                        "Эта запись будет изменена\n"
                        "1 - изменить\n"
                        "2 - отмена\n"
                        ))
                    if (finalCheck == 1):
                        dbConnection.reconnect()
                        name = input("Введите новое имя блюда\n")
                        price = int(input("Введите новую цену блюда\n"))
                        sq.updateDish(dbConnection, id, name, price)
            elif (userChoice == 6):
                id = int(input("Введите id для удаления\n"))
                found = sq.getDish(dbConnection, id)
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
                        sq.deleteDish(dbConnection, id)
            elif (userChoice == 7):
                sq.getAllClients(dbConnection)
            elif (userChoice == 8):
                name = input("Введите имя пользователя\n")
                phoneNumber = input("Введите номер телефона\n")
                addr = input("Введите адрес\n")
                sq.addNewClient(dbConnection, name, phoneNumber, addr)
            elif (userChoice == 9):
                id = int(input("Введите id пользователя\n"))
                found = sq.getClient(dbConnection, id)
                if not found:
                    print("Такой записи не существует")
                else:
                    finalCheck = int(input(
                        "Эта запись будет изменена\n"
                        "1 - изменить\n"
                        "2 - отмена\n"
                        ))
                    if (finalCheck == 1):
                        dbConnection.reconnect()
                        name = input("Введите новое имя пользователя\n")
                        phoneNumber = input("Введите новый номер телефона\n")
                        addr = input("Введите новый адрес\n")
                        sq.updateClient(dbConnection, id, name, phoneNumber, addr)
            elif (userChoice == 10):
                id = int(input("Введите id для удаления\n"))
                found = sq.getClient(dbConnection, id)
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
                        sq.deleteClient(dbConnection, id)
            else:
                print("Выбран недействительный режим работы!")
                break
        except:
            print("Завершение работы")
            break

        input("Нажмите enter для продолжения\n")

    dbConnection.close()