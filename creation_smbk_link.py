import os,random,re,datetime,logging,errno


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

##################################################

# Get UTC time
class simple_utc(datetime.tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)
    
def get_UTC_time() :
    dt_string = datetime.utcnow().replace(tzinfo=simple_utc()).isoformat()
    dt_string = str(parser.isoparse(dt_string))
    return(dt_string)

# Merge dictionary 
def Merge(dict1, dict2): 
    res = dict1.copy()   # start with x's keys and values
    res.update(dict2)    # modifies z with y's keys and values & returns None
    return(res)

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

###################################################

for root, subdirectories, files in os.walk(rootdir):

    # for subdirectory in subdirectories:

    #     print(os.path.join(root, subdirectory))

    for file in files:

        import time
        from datetime import date 

        path = (os.path.join(root, file))
       
        print('this is the raw path ',path)

        make_symb_link(path, d_file=r'/data/Server-test/data')

