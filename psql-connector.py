import os, psycopg2, json, re, datetime, time, logging


def connect(f_text=r'/tmp/sample.txt'):

    try:
        #establishing the connection
        connection = psycopg2.connect(
           user='postgres', 
           password='', 
           port= '5432'
        )
        #Creating a cursor object using the cursor() method
        cursor = connection.cursor()

        #Executing an MYSQL function using the execute() method
        cursor.execute("select version()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Connection established to: ",data)

        #Retrieving data
        # cursor.execute('''SELECT * from element where status = '20_to_transfer';''')

        cursor.execute('''SELECT name FROM element where STATUS = '20_to_transfer';''')

        #Fetching 1st row from the table
        results = cursor.fetchall()

        print("The number of parts: ", cursor.rowcount)
        for result in results:
            p_file = os.path.join('/tmp','data',  
            look_for_telescope(result[0]), 
            'DAQ', 
            'RAW', 
            look_for_date(result[0]), 
            look_for_run(result[0]), 
            result[0])

            lfn = os.path.join(os.getcwd() + p_file)
            make_path(lfn)
            make_file(lfn)
            d_file = make_symb_link(lfn)
            make_file_transfer(d_file, f_text=f_text)

    except Exception as e:
        logging.critical(e, exc_info=True)  # log exception info at CRITICAL
        pass

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

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

def look_for_sources(path) :
    
    base, file_name = os.path.split(path)
    run = str(look_for_run(file_name))

    file_name = re.findall(r'[A-Z]_([^"]*)-W', file_name)
    if not file_name: 
        file_name = os.path.basename(path)
        file_name = file_name.replace(pathlib.Path(file_name).suffix, '')

        file_name = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', file_name)

        file_name = [i for i in file_name if not i.isdigit()]
        file_name = max(file_name, key=len)    
    else :
        file_name = file_name[0].replace('+','-')
        
    if run in file_name : 
        file_name = file_name.replace(run,'')
        
    return(str(file_name))
    
def look_for_telescope(fileName):
    patterns_1 = ['M1', 'M2', 'ST']
    matching_1 = [s for s in patterns_1 if s in fileName]
    if matching_1 :
        return(str(matching_1[0]))
    
def look_for_source(path):
    base, file_name = os.path.split(path)
    run = str(look_for_run(file_name))

    file_name = re.findall(r'[A-Z]_([^"]*)-W', file_name)
    if not file_name: 
        file_name = os.path.basename(path)
        file_name = file_name.replace(pathlib.Path(file_name).suffix, '')

        file_name = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', file_name)

        file_name = [i for i in file_name if not i.isdigit()]
        file_name = max(file_name, key=len)    
    else :
        file_name = file_name[0].replace('+','-')
        
    if run in file_name : 
        file_name = file_name.replace(run,'')
        
    return(str(file_name))

###################################################
def read(file_dump='test-psql.txt', f_text=r'/tmp/sample.txt'):
    lines = open(file_dump).read().splitlines()

    try:
        for n in range(len(lines)) : 
            print()
            p_file = os.path.join('/tmp','data',  
            look_for_telescope(lines[n]), 
            'DAQ', 
            'RAW', 
            look_for_date(lines[n]), 
            look_for_run(lines[n]), 
            lines[n])

            lfn = os.path.join(os.getcwd() + p_file)
            print(lfn)  

            make_path(lfn)
            make_file(lfn)
            d_file = make_symb_link(lfn)
            make_file_transfer(d_file, f_text=f_text)
    except Exception as e:
        logging.critical(e, exc_info=True)  # log exception info at CRITICAL
        pass

def make_file(lfn, size=100000):
    file_create = open(lfn, "wb")
    file_create.seek(size)
    file_create.write(b"\0")
    file_create.close ()

def make_path(lfn):
    p_file = os.path.dirname(lfn)
    
    if not os.path.exists(p_file):
        os.makedirs(p_file)

def make_file_transfer(lfn, f_text=r'/tmp/sample.txt'):
    print('writing output file at ' + f_text)
    # Open a file with access and read mode 'a+'
    file_object = open(f_text, 'a')
    # Append 'hello' at the end of file
    file_object.write(lfn+'\n')
    # Close the file
    file_object.close()

###################################################

def make_symb_link(s_file, d_file='data_transfer'):
    # Create a symbolic link
    # pointing to src named dst
    # using os.symlink() method
    try:
        d_file = s_file.replace('data', d_file)
        make_path(d_file)
        os.symlink(s_file, d_file)
        return(d_file)
    except Exception as e:
        logging.critical(e, exc_info=True)  # log exception info at CRITICAL
        pass

if __name__ == '__main__':
    connect()
    # read()
