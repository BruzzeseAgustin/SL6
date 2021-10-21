import os,random,re,datetime,logging,errno,sys
import json, time, mysql.connector
from mysql.connector import errorcode

###################################################

def change_for_date(fileName) :
    fileName = fileName.replace('/','-')
    fileName = fileName.replace('_','-')
    
    try :
        date = re.search('\d{4}-\d{2}-\d{2}', fileName)
        date = datetime.datetime.strptime(date.group(), '%Y-%m-%d').strftime('%Y_%m_%d')
        date = datetime.datetime.strptime(date, '%Y_%m_%d')
        now = datetime.datetime.now()
        tomorrow = date.replace(year=now.year, month=now.month, day=now.day).strftime('%Y_%m_%d') 
        return(str(tomorrow))
    except : 
        pass

    if not date :      
        date = re.findall('\d{8}', fileName)
        date = datetime.datetime.strptime(date[0], '%Y%m%d').strftime('%Y%m%d')
        date = datetime.datetime.strptime(date, '%Y%m%d')
        now = datetime.datetime.now()
        tomorrow = date.replace(year=now.year, month=now.month, day=now.day).strftime('%Y%m%d')          
        return(tomorrow)
    
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
        return(datetime.datetime.strptime(date[0], '%Y%m%d').strftime('%Y%m%d'))
    
def look_for_run(fileName) :  

    try :
        run = re.search('\d{5}\.', fileName)
        if not run :
            run = re.search('_\d{5}', fileName)
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
            run = re.findall('\d{5}\_', fileName)
            run = run[0].replace('_','')
        return(str(run))
    except : 
        pass

###################################################
# Generate random run
def generate_random(lenght) :
    lower = str(1)
    upper = str(9)
    return(random.randint(int(lower.ljust(lenght, '0')), int(upper.ljust(lenght, '9'))))

###################################################

def make_path(lfn):
    print(lfn)
    path_file = os.path.dirname(lfn)
    
    if not os.path.exists(path_file):
        print(path_file)
        os.makedirs(path_file)

def make_file(file_name, dest, size = 1000000):
    file_create = open(file_name, "wb")
    file_create.seek(size)
    file_create.write(b"\0")
    file_create.close ()
    
def make_symb_link(s_file, d_file='/data_transfer'):
    # Create a symbolic link
    # pointing to src named dst
    # using os.symlink() method
    if not os.path.exists(d_file):

        # Create a new directory because it does not exist 
        os.makedirs(d_file)
        
    
    '''   
    try:
        # make_path(d_file)
        # symb_file = construct_file(s_file)
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
    '''
    
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
            

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row
            
def search(config, sql_query, values):
    print("Going to describe Table ")    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("SHOW FULL TABLES;")
        for table in cursor:
            print(table)

        print()
        result = cursor.execute(sql_query, values)
        return(result)
    
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


def make_file_transfer(list_lfn, mode='a', output_file=r'sample.txt'):
    
    print('writing output file at ' + output_file)
    # Open a file with access and read mode 'a+'
    file_object = open(output_file, mode)
    # Append 'hello' at the end of file
    
    for lfn in list_lfn:
        print(lfn)        
        file_object.write(lfn+'\n')
        # Close the file
    
    file_object.close()
                        
def get_random_line(dump_file):
    file = random.choice(open(dump_file).read().splitlines())     
    filename, file_extension = os.path.splitext(file)
    if '.root' in file_extension or '.gz' in file_extension or '.h5' or '.fz' or 'fits' :
        return(file)
    else :
        get_random_line(dump_file)

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def human_read_to_byte(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

###################################################

if __name__ == '__main__':

    config = {
        'user': 'root',
        'host': 'localhost',
        'password': '',
        'database': 'magic',
        'raise_on_warnings': True
    }
    
    number_lines = 10 
    dump_file = 'CTA_dataset.txt'
    size_file = 1000
    rootdir = './fefs/'
    symbdir = './fefs/data/Other/rucio_tmp/Server-test/data'

    if sys.argv[1] == "update" : 
        sql_query = ("SELECT S.FILE_PATH, S.FILE_TYPE, T.DATE_DISCOVERED, T.TRANSFER_STATUS FROM STORAGE AS S, "
                     "TRANSFER AS T WHERE S.ID = T.STORAGE_ID AND T.TRANSFER_STATUS LIKE 'DONE%' AND T.STORAGE_ID;")  


        add_entry = ("INSERT INTO TRANSFER (STORAGE_ID, DATE_DISCOVERED, TRANSFER_STATUS) VALUES " 
                "((SELECT ID from STORAGE where FILE_PATH LIKE %s) "
                ", %s, %s);")

        relevant_path = '/data/'
        match_name = r'Transfer_done-'
        
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute("SHOW FULL TABLES;")
            for table in cursor:
                print(table) 

            print()
            cursor.execute(sql_query) 

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
                    idx_to_delete = []
                    for line in lines:
                        print(count, '-', len(lines)-1 )

                        parts = line.split() # split line into parts
                        print(parts)
                        if len(parts) > 1:   # if at least 2 parts/columns
                            file_name = "%"+os.path.basename(parts[0])
                            print(file_name)
                            date_to_be_change = parts[1]
                            datetime_object = datetime.datetime.strptime(date_to_be_change, '%Y-%m-%dT%H:%M:%S.%fZ')
                            datetime_object = datetime.datetime.strftime(datetime_object, '%Y-%m-%d %H:%M:%S')

                            i = 1
                            for row in iter_row(cursor, 10):
                                print(row[0])

                                if file_name in row[0] :
                                    print('going to delete index: ',count)
                                    idx_to_delete.append(count)
                                    break
                                elif file_name not in row[0]:   
                                    val = (file_name, datetime_object, "DONE")
                                    print(val)
                                    response = update_file_status(config, add_entry, val)    
                                    print(response)
                                    if response == True :
                                        print('going to delete index: ',count)
                                        idx_to_delete.append(count)
                                        break
                                        
                                i = i +1                                

                        count += 1
                    print(idx_to_delete)
                    for idx in sorted(idx_to_delete, reverse=True):
                        del lines[idx] 
                    lines = [s.rstrip() for s in lines] # remove \r
                    lines = list(filter(None, lines)) # remove empty 
                    # print(lines, file, len(lines))
                    make_file_transfer(lines, 'w+', n_file) 


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
            
            
    elif sys.argv[1] == "create" : 

        for row in range(number_lines):
            random_file = get_random_line(dump_file)

            # Check whether the 
            # specified path is an
            # absolute path or not
            if os.path.isabs(random_file) :
                random_file = os.path.relpath(random_file, '/')

            file = os.path.join(rootdir, random_file)

            make_path(file) # this will go out
            make_file(file, size_file)  

            print('file %s of %s created at %s' %(file, human_read_to_byte(size_file), rootdir))
    

                
    elif sys.argv[1] == "symb":
        import time
        from datetime import date 

        for path, subdirs, files in os.walk(rootdir):
            for name in files:
                print(os.path.join(path, name))
                path_file = os.path.join(path, name)
                symblink_file = os.path.join(path, name)
                run = look_for_run(path_file)
                get_old_date = look_for_date(path_file)
                get_current_date = change_for_date(path_file)
                new_run = str(generate_random(len(run)))

                # Get the base name 
                # of the specified path
                try : 
                    date_file_basename = look_for_date(os.path.basename(path_file))
                    if date_file_basename is not None: 
                            get_current_basename_date = change_for_date(date_file_basename)
                            symblink_file = symblink_file.replace(date_file_basename, get_current_basename_date)

                except:
                    pass

                print(get_old_date, get_current_date)
                print(run, new_run)

                symblink_file = symblink_file.replace(get_old_date, get_current_date)
                symblink_file = symblink_file.replace(run, new_run)
                symblink_file = symblink_file.replace(rootdir, os.path.join(symbdir, ''))

                if not os.path.exists(symbdir):

                    # Create a new directory because it does not exist 
                    os.makedirs(symbdir)

                make_path(symblink_file)

                print(os.path.abspath(path_file), os.path.abspath(symblink_file))
                os.symlink(os.path.abspath(path_file), os.path.abspath(symblink_file))
                print()

                ###################################
                val = (symblink_file,)        
                add_entry = ("INSERT INTO STORAGE "
                   "(FILE_PATH) "
                   "VALUES (%s)")

                # connect(config, add_entry, val)

                ###################################
                val = (symblink_file, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), "PENDING")         
                add_entry = ("INSERT INTO TRANSFER (STORAGE_ID, DATE_DISCOVERED, TRANSFER_STATUS) VALUES " 
                             "((SELECT ID from STORAGE where FILE_PATH LIKE %s) "
                             ", %s, %s);")

                # connect(config, add_entry, val)  
