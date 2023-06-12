# Project Name     : Canteen Ordering System
# Made by          : Jenil Rathod, Ankush Jaykar, Suyash Kadam, Gauri Kshirsagar, Atharva Kulkarni & Samarpita Kule
# Roll no.         : 2107, 2106, 2110, 2125, 2126 & 2127
import mysql.connector
from datetime import date
from datetime import datetime
import pywhatkit
from PIL import Image

user = 'Anonymous'
manager = 'Anonymous'


def clear():
    """Creates a Blank area """
    for space in range(65):
        print()


def Existing_items():
    """Show's Existing Items"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    sql = 'select * from canteens;'
    cursor.execute(sql)
    record = cursor.fetchall()
    while True:
        print("0 Exit")
        for can in record:
            print(can[0], can[1])
        choice = int(input("Enter choice :"))
        if choice == 0:
            print("Returning to main menu....")
            input("Press any key to continue........")
            break
        else:
            sql = 'select * from ' + str(record[int(choice)-1][1]) + ';'
            cursor.execute(sql)
            record1 = cursor.fetchall()
            for a, b, c in record1:
                print(a, '\t', b, '\t', c)
        further = input("Do you wanna continue[y/n]?")
        if further == 'n' or further == "N":
            print("Press any key to continue.....")
            break


def main_menu():
    """Function  for main menu"""
    while True:
        clear()
        print("- " * 33)
        print("|", " " * 61, "|")
        print("|                    Welcome to Zeal college Canteen            |")
        print("\n1. Order\n2. Available Items\n3. Bill Generation\n4. Recent Orders\n5. Logout\n\n")
        choice = int(input("Enter your Choice...:  "))
        if choice == 1:
            order(user)
        elif choice == 2:
            Existing_items()
        elif choice == 3:
            bill(user)
        elif choice == 4:
            recent_order(user)
        elif choice == 5:
            input("\n\n\n Press any key to continue.....")
            break
        else:
            print("Invalid Input")


def customer_exists(user_id, password):
    """Checks if Already a customer"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor()
    sql = 'select * from customer where user_id = "' + user_id + '" and password = "' + password + '";'
    cursor.execute(sql)
    record = cursor.fetchone()
    return record


def add_customer():
    """Adds customer"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor()
    clear()
    print("New Login Page")
    user_id = input('Enter user_id:')
    password = input("Enter password:")
    if customer_exists(user_id, password) is None:
        sql = 'insert into customer( user_id, password) values ("' + user_id + '","' + password + '");'
        cursor.execute(sql)
        conn.commit()
        input(f'Welcome {user_id}')
    else:
        print('Customer already exists.....')
        input('Returning to Main menu')
    conn.close()


def account():
    """Select whether already a customer or new customer"""
    clear()
    print("- " * 33)
    print("|", " " * 61, "|")
    print("|                    Welcome to Zeal college Canteen            |")
    print("\n1.Already a Customer \n2. Sign up \n3. Exit")
    choice = int(input("Enter your Choice...:  "))
    if choice == 1:
        user_id = input('Enter user_id:')
        password = input("Enter password:")
        a = customer_exists(user_id, password)
        if a == (user_id, password):
            input(f'Welcome {user_id}........... ')
            global user
            user = user_id
            main_menu()
        else:
            input("The Customer doesn't exit's.....")
    elif choice == 2:
        add_customer()
    elif choice == 3:
        input('Returning to main menu')
        start()
    else:
        print('Invalid Input')


def order(user_id):
    """Order's food items"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    sql = 'select * from canteens;'
    cursor.execute(sql)
    record = cursor.fetchall()
    while True:
        print("0 Exit")
        for can in record:
            print(can[0], can[1])
        choice = int(input("Enter choice :"))
        if choice == 0:
            print("Returning to main menu.......")
            break
        elif choice > len(record):
            print("Invalid choice......\n\n\n")
        else:
            price = 0
            sql = 'select * from ' + str(record[int(choice - 1)][1]) + ';'
            cursor.execute(sql)
            record1 = cursor.fetchall()
            for a, b, c in record1:
                print(a, '\t', b, '\t', c)
            n = int(input("enter number of items to order:"))
            item = ''
            a = 0
            while a < n:
                Sr_no = int(input("enter order id:"))
                if Sr_no > len(record1):
                    print("Item doesn't exist...\n\n\n")
                else:
                    item += record1[Sr_no - 1][1] + '  '
                    sql1 = 'select price from ' + str(record[int(choice - 1)][1]) + ' where Sr_no = ' + str(Sr_no) + ';'
                    cursor.execute(sql1)
                    net = cursor.fetchone()
                    price += int(net[0])
                    a += 1
            name = user_id
            sql3 = 'insert into bills(User_id, Canteen,Item, price, doo) values (%s,%s,%s,%s,%s);'
            values = (str(name), str(record[0][1]), item, str(price), str(date.today()))
            cursor.execute(sql3, values)
            conn.commit()

            further = input("Do you wanna continue[y/n]?")
            if further == 'n' or further == "N":
                now = datetime.now()
                time_now = now.strftime("%H:%M:%S")
                hr = int(time_now[0:2])
                minutes = int(time_now[3:5])+1
                pywhatkit.sendwhatmsg(str(record[int(choice - 1)][2]), item, hr, minutes)
                break


def bill(user_id):
    """Generates Bills"""
    clear()
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    sql = 'select User_id, Canteen, Item, price, doo from bills where User_id = %s  and doo = %s;'
    values = (str(user_id), str(date.today()))
    cursor.execute(sql, values)
    record = cursor.fetchall()
    if not record:
        input("No recent order exists.......")
    else:
        print("\t\t\t\tZeal Canteen, Narhe, Pune")
        print("\t\t\tPhone no.: 9182736455,9132418221")
        print("\t\t\t\tGSTIN: 07AAECR2971C1Z")
        print(f"\t\t\tDate: {datetime.now()}")
        print("\t\t Canteen\t\tItems\t\tRate\t\tAmount")
        amount = 0
        for total in record:
            print("\t\t", total[1], "\t\t", total[2], "\t\t\t", total[3], "\t\t\t",
                  float(total[3]) + float(total[3]) * 0.18)
            amount += float(total[3]) + float(total[3]) * 0.18
        print("\t", "-" * 45)
        print("\t\t Total: \t\t\t\t\t\t", int(amount))
        print("\n\n\n")
        pay = input("Do you wanna by by cash/online:")
        if pay == "online":
            image = Image.open("jenilpay.jpg")
            image.show()
        else:
            print(f"Payable amount = {amount}")
        input("thankyou visit again............")
        items = ''
        for item in record:
            items += item[2] + ' '
        print(type(items))
        sql = 'insert into paid_bills (User_id, Amount, Doo,Item) values(%s,%s,%s,%s);'
        value = (str(user_id), str(amount), str(date.today()), str(items))
        cursor.execute(sql, value)
        conn.commit()


def recent_order(user_id):
    """Show's Recent order from the provided date"""
    clear()
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    dos = input("Date of recent orders[yyyy-mm=dd]: ")
    sql = 'select * from paid_bills where User_id = %s and Doo > %s'
    value = (str(user_id), dos)
    cursor.execute(sql, value)
    record = cursor.fetchall()
    if not record:
        input("No recent orders........")
    else:
        for rec in range(len(record)):
            print(record[rec][4], "\t\t", record[rec][3], "\t\t", record[rec][2])
        input("Press any key to continue........")
    pass


def can_main_menu():
    """Function for canteen manager"""
    while True:
        clear()
        print("- " * 33)
        print("|", " " * 61, "|")
        print("|                    Welcome to Zeal college Canteen            |")
        print("\n1. Add Items\n2. Update Items Price\n3. Remove Items\n4. Bills\n5. Revenue Generated\n6. Logout")
        choice = int(input("Enter your Choice...:  "))
        if choice == 1:
            add_item(manager)
        elif choice == 2:
            update_Items(manager)
        elif choice == 3:
            remove_item(manager)
        elif choice == 4:
            bill_manager(manager)
        elif choice == 5:
            revenue_generated(manager)
        elif choice == 6:
            input("\n\n\n Press any key to continue.....")
            break
        else:
            print("Invalid Input")


def manager_exists(user_id, password):
    """Check's the Existing Manager"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor()
    sql = 'select * from manager where user_id = "' + user_id + '" and password = "' + password + '";'
    cursor.execute(sql)
    record = cursor.fetchone()
    return record


def add_manager():
    """Adds customer"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    clear()
    print("New Login Page")
    user_id = input('Enter user_id:')
    password = input("Enter password:")
    no = input("enter number")
    if manager_exists(user_id, password) is None:
        sql = 'insert into manager( user_id, password) values ("' + user_id + '","' + password + '");'
        cursor.execute(sql)
        conn.commit()
        input(f'Welcome {user_id}')
        sql1 = 'create table ' + str(
            user_id) + '  (Sr_no int primary key, Item_name varchar(50), Price float);'
        sql2 = 'insert into canteens (Name,Number) values(%s,%s);'
        values = (str(user_id), no)
        cursor.execute(sql1)
        cursor.execute(sql2, values)
        conn.commit()
    else:
        print('Customer already exists.....')
        input('Returning to Main menu')
    conn.close()


def manager_account():
    """Select whether already a manager or not manager"""
    clear()
    print("- " * 33)
    print("|", " " * 61, "|")
    print("|                    Welcome to Zeal college Canteen            |")
    print("\n1.Already a Manager \n2. Sign up \n3. Exit")
    choice = int(input("Enter your Choice...:  "))
    if choice == 1:
        user_id = input('Enter user_id:')
        password = input("Enter password:")
        a = manager_exists(user_id, password)
        if a == (user_id, password):
            input(f'Welcome {user_id}........... ')
            global manager
            manager = user_id
            can_main_menu()
        else:
            input("The Manager doesn't exit's.....")
    elif choice == 2:
        add_manager()
    elif choice == 3:
        input('Returning to main menu')
        start()
    else:
        print('Invalid Input')


def add_item(manager_id):
    """Used to add items"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    clear()
    sql = 'select * from ' + str(manager_id) + ';'
    cursor.execute(sql)
    record = cursor.fetchall()
    for i, j, k in record:
        print(f"{i}  {j}  {k}")
    print("\n\n Insert the details of new items")
    Sr_no = int(input("Enter order id:"))
    item = input("Enter item name:")
    price = float(input("Enter thr price of item:"))
    sql1 = 'insert into ' + str(manager_id) + ' values(%s,%s,%s);'
    values = (str(Sr_no), item, str(price))
    cursor.execute(sql1, values)
    conn.commit()
    input("Item added Successfully...")


def update_Items(manager_id):
    """Used for updating items"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    clear()
    sql = 'select * from ' + str(manager_id) + ';'
    cursor.execute(sql)
    record = cursor.fetchall()
    for i, j, k in record:
        print(f"{i}  {j}  {k}")
    sr_no = int(input("Enter order id of item to be updated:"))
    print("\n\nInsert the details of item to be updated")
    Sr_no = int(input("Enter order id:"))
    item = input("Enter item name:")
    price = float(input("Enter thr price of item:"))
    sql1 = 'update ' + str(manager_id) + ' set Sr_no = %s, Item_no = %s, price = %s where Sr_no = %s;'
    values = (str(Sr_no), item, str(price), str(sr_no))
    cursor.execute(sql1, values)
    conn.commit()
    input("Updated Successfully......")


def remove_item(manager_id):
    """Used to Remove items"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    clear()
    sql = 'select * from ' + str(manager_id) + ';'
    cursor.execute(sql)
    record = cursor.fetchall()
    print(f"\n\n Available Items")
    for i, j, k in record:
        print(f"{i}  {j}  {k}")
    Sr_no = int(input("Enter the id of the item to remove:"))
    sql1 = 'delete from ' + str(manager_id) + ' where Sr_no = ' + str(Sr_no) + ';'
    cursor.execute(sql1)
    conn.commit()
    input("Item added successfully.......")


def bill_manager(manager_id):
    """Bills of the manager"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    clear()
    sql = 'select User_id, price, Doo from bills where Canteen = %s;'
    values = (str(manager_id),)
    cursor.execute(sql, values)
    record = cursor.fetchall()
    print("List of Bills\n\n")
    for i, j, k in record:
        print(f"{i}  {j}  {k}")
    input("Press any key to continue....")


def revenue_generated(mana_id):
    """Show's Revenue of the manager"""
    conn = mysql.connector.connect(host='localhost', database='canteen', user='root', password='Jenil_7828')
    cursor = conn.cursor(buffered=True)
    clear()
    date_order = input("Revenue to be generated from: ")
    price = 0
    sql = 'select price from bills where Canteen = %s and Doo >= %s;'
    values = (str(mana_id), date_order)
    cursor.execute(sql, values)
    record = cursor.fetchall()
    for i in record:
        price += int(i[0])
    print(f"\n\nTotal Collection Made:{price}")
    input("press any key to continue......")


def start():
    """Select whether customer or Canteen Owner"""
    while True:
        clear()
        print("- " * 33)
        print("|", " " * 61, "|")
        print("|                    Welcome to Zeal college Canteen            |")
        print("\n1. Customer \n2. Canteen Manager \n3. Exit")
        choice = int(input("Enter your Choice...:  "))
        if choice == 1:
            account()
        elif choice == 2:
            manager_account()
        elif choice == 3:
            input("\n\n\nThank you for Visiting................")
            break
        else:
            print("Invalid Input")


start()
