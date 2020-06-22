import sqlite3
import random
db = sqlite3.connect('database2_new.db')
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
# print(tables)
detail = {}

for table_name in tables:
    query = "SELECT Count(*) from " + table_name[0] + ";"
    cursor.execute(query)
    detail[table_name[0]] = cursor.fetchall()[0][0]

Table = []
TotalNumberofRows = 0
for item in detail:
    TotalNumberofRows = TotalNumberofRows + detail[item]
    Table.append(item)

tablecolumn = {
    'orderdetails': {'products': 'productCode', 'orders': 'orderNumber'},
    'productlines': {'products': 'productLine'},
    'orders': {'customers': 'customerNumber', 'orderdetails': 'orderNumber'},
    'payments': {'customers': 'customerNumber'},
    'products': {'productlines': 'productLine', 'orderdetails': 'productCode'},
    'offices': {'employees': 'officeCode'},
    'employees': {'customers': 'employeeNumber'},
    'customers': {'orders': 'customerNumber', 'payments': 'customerNumber'}
}

selectivitytable=[round(random.uniform(0, 1)/10,4) for _ in range(len(detail))]
# print(selectivitytable)



def selectivityUtil(table1, table2, column1):
    # selectivtiy of join is car(join)/max(card(a),card(b):
    sql = 'SELECT  count(DISTINCT ' + table1 + '.' + column1 + ' )  from ' + table1 + "  JOIN " + table2 + " ON " + table1 + '.' + column1 + " = " + table2 + '.' + column1 + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    j = result[0][0]

    sql = "Select count(*) from " + table1 + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    t1 = result[0][0]

    sql = "Select count(*) from " + table2 + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    t2 = result[0][0]

    sel = round(j / max(t1, t2), 4)

    Nt = round(t1 * sel / TotalNumberofRows, 4)

    return Nt


def CLPC(database):
    sel = []
    for table1 in database:
        for table2 in database[table1]:
            column = database[table1][table2]
            sel.append(selectivityUtil(table1, table2, column))
            # print(table1, 'join', table2, ':', column, selectivityUtil(table1, table2, column))
    return max(sel)


ClpcOfDatabase = CLPC(tablecolumn)

print("Details of the Databsae:\n")
print("Tables:", detail)
print("Sum of all Tuples", TotalNumberofRows)
print('CLPC of the database:', ClpcOfDatabase)

# sql = 'SELECT COUNT(DISTINCT officeCode) FROM employees;'
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)
#
# sql = 'SELECT COUNT(*) FROM employees;'
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)

cursor.close()
db.close()