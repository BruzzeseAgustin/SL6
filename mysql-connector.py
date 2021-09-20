import os, json, re, datetime, time, logging, mysql.connector, errno
from mysql.connector import errorcode

def connect(config, d_file=r'/data_transfer', f_text=r'/tmp/sample.txt'):
    print("Going to describe Table ")    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("SHOW FULL TABLES;")
        for table in cursor:
            print(table) 

        print()
        cursor.execute("SELECT S.FILE_PATH, S.FILE_TYPE, T.DATE_DISCOVERED, T.TRANSFER_STATUS FROM STORAGE AS S, TRANSFER AS T WHERE S.ID = T.STORAGE_ID AND T.TRANSFER_STATUS LIKE 'PENDING%' AND T.STORAGE_ID  NOT IN (SELECT T.STORAGE_ID FROM TRANSFER AS T WHERE T.TRANSFER_STATUS LIKE 'DONE%');") 

        # loop through the rows
        i = 1
        for row in iter_row(cursor, 10):
            # print(str(i) + '-' + ' ' + row)
            print(row[0])
            make_path(row[0]) # this will go out
            make_file(row[0])
            try:
                d_p_file = make_symb_link(row[0], d_file=d_file)
                make_file_transfer(d_p_file, f_text=f_text)
            except OSError as e:
                print(e)
                pass
            i = i +1

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


###################################################

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def make_file(lfn, size=100000):
    file_create = open(lfn, "wb")
    file_create.seek(size)
    file_create.write(b"\0")
    file_create.close ()

def make_path(lfn):
    print(lfn)
    path_file = os.path.dirname(lfn)
    
    if not os.path.exists(path_file):
        print(path_file)
        os.makedirs(path_file)

def make_file_transfer(lfn, f_text=r'/tmp/sample.txt'):
    print('writing output file at ' + f_text)
    # Open a file with access and read mode 'a+'
    file_object = open(f_text, 'a')
    # Append 'hello' at the end of file
    file_object.write(lfn+'\n')
    # Close the file
    file_object.close()

###################################################

def make_symb_link(s_file, d_file='/data_transfer'):
    # Create a symbolic link
    # pointing to src named dst
    # using os.symlink() method
    d_file = s_file.replace('/data', d_file)
    try:
        make_path(d_file)
        os.symlink(s_file, d_file)
        return(d_file)
    except Exception as e:
        logging.critical(e, exc_info=True)  # log exception info at CRITICAL
        if e.errno == errno.EEXIST:
            os.remove(d_file)
            os.symlink(s_file, d_file)
            return(d_file)   
        else:
            raise e      
    except OSError as e:

            os.remove(d_file)
            os.symlink(s_file, d_file)
            logging.critical(e, exc_info=True)  # log exception info at CRITICAL

###################################################

if __name__ == '__main__':

    config = {
        'user': 'root',
        'host': 'localhost',
        'password': '',
        'database': 'magic',
        'raise_on_warnings': True
    }
    connect(config, d_file=r'/data/Other/rucio_tmp/Server-test/data', f_text=r'/data/sample.txt')
