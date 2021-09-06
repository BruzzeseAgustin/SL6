import mysql.connector
from mysql.connector import errorcode

def connect(config):
    print("Going to describe Table ")    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("SHOW FULL TABLES;")
        for table in cursor:
            print(table) 

            print()
        cursor.execute("SELECT S.FILE_PATH, S.FILE_TYPE, T.DATE_DISCOVERED, T.TRANSFER_STATUS FROM storage.STORAGE AS S, transfer.TRANSFER AS T WHERE S.ID = T.STORAGE_ID AND T.TRANSFER_STATUS LIKE 'PENDING%' LIMIT 50;") 
        # fetch all the matching rows 
        result = cursor.fetchmany(12)
        # loop through the rows
        for row in result:
            print(row)
            print("\n")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        if cnx.is_connected():
            cnx.close()
            cursor.close()
            print("MySQL connection is closed")

if __name__ == '__main__':

    config = {
        'user': 'root',
        'host': 'localhost',
        'password': '',
        'database': 'magic',
        'raise_on_warnings': True
    }
    connect(config)
