import os,random,re,datetime,logging,errno,sys
import json, time, mysql.connector
from mysql.connector import errorcode


rootdir = '/data/M1'

###################################################

def look_for_date(fileName) :
    fileName = fileName.replace('/','-')
    fileName = fileName.replace('_','-')
    date = []
    try :
        date = re.search('\d{4}-\d{2}-\d{2}', fileName)
        date = datetime.datetime.strptime(date.group(), '%Y-%m-%d').strftime('%Y_%m_%d')
        return(str(date))
    except : 
        pass

    if not date :
        date = re.findall('\d{8}', fileName)   
        return(datetime.datetime.strptime(date[0], '%Y%m%d').strftime('%Y_%m_%d'))
    
def look_for_run(fileName) :  

    try :
        run = re.search('\d{8}\.', fileName)
        if not run :
            run = re.search('_\d{8}', fileName)
            run = run[0].replace('_','')
        elif (type(run).__module__, type(run).__name__) == ('_sre', 'SRE_Match') : 
            run = run.group(0)
            run = run.replace('.','')
        else :
            run = run[0].replace('.','')
            
        return(str(run))
    except : 
        pass
    
    try :
        if not run :
            run = re.findall('\d{8}\_', fileName)
            run = run[0].replace('_','')
        return(str(run))
    except : 
        pass


# Generate random run
def generate_random() :
    return(random.randint(10000000,99999999))

###################################################

def make_path(lfn):
    print(lfn)
    path_file = os.path.dirname(lfn)
    
    if not os.path.exists(path_file):
        print(path_file)
        os.makedirs(path_file)

def make_symb_link(s_file, d_file='/data_transfer'):
    # Create a symbolic link
    # pointing to src named dst
    # using os.symlink() method

    try:
        # make_path(d_file)
        symb_file = construct_file(s_file)
        symb_file = symb_file.replace('/data', d_file)
        make_path(symb_file)
        print('this is the modified path ', symb_file)
        os.symlink(s_file, symb_file)
        return(symb_file)
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

def construct_file(path):
    try:
        date = re.search('\d{4}_\d{2}_\d{2}', path)
        date = datetime.datetime.strptime(date.group(), '%Y_%m_%d').date()
        date = date.strftime('%Y_%m_%d')
        today = str(time.strftime('%Y_%m_%d'))
        path = os.path.join('/',path.replace(date, today))
    except: 
        pass
    try:
        base, name = os.path.split(path)  
        file_name = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', name)
        date = datetime.datetime.strptime(file_name[0], "%Y%m%d").date()
        date = date.strftime('%Y%m%d') 
        today = str(time.strftime('%Y%m%d'))
        path = os.path.join('/',path.replace(date, today))
    except:
        pass     

    try:
        run = look_for_run(path)
        path = path.replace(run, str(generate_random()))
    except:
        pass
    return(path)

#################################################

def connect(config, sql_query, values):
    print("Going to describe Table ")    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("SHOW FULL TABLES;")
        for table in cursor:
            print(table)

        print()
        '''
        add_entry = ("INSERT INTO STORAGE "
           "(FILE_PATH) "
           "VALUES (%s)")
        val = (symblink_file,)
        '''
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
            
###################################################

def check_file_entry(config, sql_query, values):
    print("Going to describe Table ")    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("SHOW FULL TABLES;")
        for table in cursor:
            print(table)

        print()

        print(sql_query, values)
        cursor.execute(sql_query, values)
        if len(cursor.fetchall()) >= 1:
            return(True)
        else :
            return(False)
        
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

    print(rootdir)


    config = {
        'user': 'root',
        'host': 'localhost',
        'password': '',
        'database': 'magic',
        'raise_on_warnings': True
    }
    
    for idx, arg in enumerate(sys.argv):
        #print("Argument #{} is {}".format(idx, arg))
       
        if arg == "symb":
            for root, subdirectories, files in os.walk(rootdir):

                for file in files:
                    print(file)
                    import time
                    from datetime import date 

                    path = (os.path.join(root, file))

                    print('this is the raw path ',path)

                    symblink_file = make_symb_link(path, d_file=r'/data/Other/rucio_tmp/Server-test/data')

                    ###################################
                    val = (symblink_file,)        
                    add_entry = ("INSERT INTO STORAGE "
                       "(FILE_PATH) "
                       "VALUES (%s)")

                    connect(config, add_entry, val)

                    ###################################
                    val = (symblink_file, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), "PENDING")         
                    add_entry = ("INSERT INTO TRANSFER (STORAGE_ID, DATE_DISCOVERED, TRANSFER_STATUS) VALUES " 
                                 "((SELECT ID from STORAGE where FILE_PATH LIKE %s) "
                                 ", %s, %s);")

                    connect(config, add_entry, val)  

        elif arg == "update" :   

            add_entry = ("INSERT INTO TRANSFER (STORAGE_ID, DATE_DISCOVERED, TRANSFER_STATUS) VALUES " 
                "((SELECT ID from STORAGE where FILE_PATH LIKE %s) "
                ", %s, %s);")
            
            check_entry = ("SELECT * FROM TRANSFER WHERE STORAGE_ID LIKE (SELECT ID FROM STORAGE where FILE_PATH LIKE %s) AND TRANSFER_STATUS LIKE %s;")

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
                    idx_to_delete = []
                    for line in lines:
                        print(count, '-', len(lines)-1 )
                        # print("Line{}: {}".format(count, line.replace("\n", "").strip()))     
                        parts = line.split() # split line into parts
                        if len(parts) > 1:   # if at least 2 parts/columns
                            file_name = "%"+os.path.basename(parts[0])
                            date_to_be_change = parts[1]
                            datetime_object = datetime.datetime.strptime(date_to_be_change, '%Y-%m-%dT%H:%M:%S.%fZ')
                            datetime_object = datetime.datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')

                            val = (file_name, "DONE")
                            check = check_file_entry(config, check_entry, val)    
                            print(check)
                            
                            if check == False:   
                                val = (file_name, datetime_object, "DONE")
                                print(val)
                                response = update_file_status(config, add_entry, val)    
                                print(response)
                                if response == True :
                                    print('going to delete index: ',count)
                                    idx_to_delete.append(count)
                            elif check == True :
                                print('going to delete index: ',count)
                                idx_to_delete.append(count)
                            
                        count += 1
                    for idx in sorted(idx_to_delete, reverse=True):
                        del lines[idx] 
                        
                    lines = [s.rstrip() for s in lines] # remove \r
                    lines = list(filter(None, lines)) # remove empty 
                    # print(lines, file, len(lines))
                    if len(lines) >= 1 :
                        make_file_transfer(lines, n_file) 

                    new_file.close()
