import os, json, re, datetime, time, logging, mysql.connector, errno, sys
from mysql.connector import errorcode

def discover_files(config, d_file=r'/data_transfer'):
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


def check_transfers_rucio(input_file):
    if os.path.isfile(input_file):
        file = open(input_file, "r+")
        lines = file.readlines()
        
        count = []
        for line in lines:
            print("Line{}: {}".format(count, line.replace("\n", "").strip()))     
            parts = line.split() # split line into parts
            if len(parts) > 1:   # if at least 2 parts/columns
                file_name = parts[0]
                date_to_be_change = parts[1]
                print(file_name, date_to_be_change)
                datetime_object = datetime.datetime.strptime(date_to_be_change, '%Y-%m-%dT%H:%M:%S.%fZ')
                datetime_object = datetime.datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')
                print(file_name, datetime_object)

def update_file_status(config, sql_query, values):
    print("Going to update Table ")    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        print(sql_query, values)
        cursor.execute(sql_query, values)
        cnx.commit()
 
        print(cursor.rowcount, "record inserted.")

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
            return(True)


def make_file_transfer(list_lfn, output_file=r'sample.txt'):
    
    print('writing output file at ' + output_file)
    # Open a file with access and read mode 'a+'
    file_object = open(output_file, 'a')
    # Append 'hello' at the end of file
    
    for lfn in list_lfn:
        print(lfn)        
        file_object.write(lfn+'\n')
        # Close the file
    
    file_object.close()
    
###################################################

if __name__ == '__main__':

    config = {
        'user': 'root',
        'host': 'localhost',
        'password': '',
        'database': 'magic',
        'raise_on_warnings': True
    }

    for idx, arg in enumerate(sys.argv):
        print("Argument #{} is {}".format(idx, arg))
       
        if arg == "discover":
            
            discover_files(config, d_file=r'/data/Other/rucio_tmp/Server-test/data')

        elif arg == "update" :   

            add_entry = ("INSERT INTO TRANSFER (STORAGE_ID, DATE_DISCOVERED, TRANSFER_STATUS) VALUES " 
                "((SELECT ID from STORAGE where FILE_PATH LIKE %s) "
                ", %s, %s);")

            relevant_path = '/data/'
            match_name = r'Transfer_done-'
            files = [f for f in os.listdir(relevant_path) if re.match(match_name, f)]
            for n_file in files: 
                print(file)
                n_file = os.path.join(relevant_path, n_file)
                print(n_file)
                if os.path.getsize(n_file) == 0: 
                    print(n_file)
                    os.remove(n_file)  
                else:
                    file = open(n_file, "r+")
                    lines = file.readlines()
                    file.close()
        
                    count = 0
                    new_file = open(n_file, "w+")
                    for line in lines:
                        # print("Line{}: {}".format(count, line.replace("\n", "").strip()))     
                        parts = line.split() # split line into parts
                        if len(parts) > 1:   # if at least 2 parts/columns
                            file_name = "%"+os.path.basename(parts[0])
                            date_to_be_change = parts[1]
                            datetime_object = datetime.datetime.strptime(date_to_be_change, '%Y-%m-%dT%H:%M:%S.%fZ')
                            datetime_object = datetime.datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')
                            # print(file_name, datetime_object)

                            val = (file_name, datetime_object, "DONE")
                            print(val)
                            response = update_file_status(config, add_entry, val)    
                            print(response)
                            if response == True :
                                print(count)
                                del lines[count]
                        count += 1
                    lines = [s.rstrip() for s in lines] # remove \r
                    lines = list(filter(None, lines)) # remove empty 
                    # print(lines, file, len(lines))
                    if len(lines) >= 1 :
                        make_file_transfer(lines, n_file) 

                    new_file.close()
