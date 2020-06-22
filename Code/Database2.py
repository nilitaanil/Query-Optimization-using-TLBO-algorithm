import sqlite3

conn = sqlite3.connect('/home/pachi/PycharmProjects/DBproj/database2_new.db')
c = conn.cursor()
print("Connection Opnend!")

print("reading commands!\n\n")

fd = open('database_latest.sql', 'r')
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# Execute every command from the input file
value = 0
print("excecuting Commands\n\n")
for command in sqlCommands:
    command = command + ';'
    print(command)
    c.execute(command)
    value = value + 1

conn.commit()
conn.close()
print("closed connection")
