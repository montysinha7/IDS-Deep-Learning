import pymysql
import sys
import csv
import pandas as pd
import subprocess
from datetime import datetime
import pysftp

def runcapture():
    cmd = ["/home/monty/Documents/extractorscript.sh"]
    print("running capture script ",cmd,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    proc = subprocess.call(cmd)
    print("capture complete",datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


def mysql_to_csv(sql, file_path, host, user, password):
    '''
    The function creates a csv file from the result of SQL
    in MySQL database.
    '''
    try:
        con = pymysql.connect(host=host,
                                user=user,
                                password=password)
        print('Connected to DB: {}'.format(host))
        # Read table with pandas and write to csv
        df = pd.read_sql(sql, con)
        df.to_csv(file_path, encoding='utf-8', header = True,\
         doublequote = True, sep=',', index=False)
        print('File, {}, has been created successfully'.format(file_path))
        con.close()

    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)

def mergefilesdata(mysqlextract,k99featureextract,output):
    path_to_csv=k99featureextract #"/home/monty/Documents/extractdata/capturenormal.csv"
    data=pd.read_csv(path_to_csv, encoding='utf-8',header=None)
    data = data.iloc[:,:30]
    data['ip_addressport']=data[28]+':'+data[29].astype(str)
    data.drop(28,axis=1)
    data.drop(29,axis=1)
    path_to_csv1=mysqlextract #"../extractdata/mysqlexport.csv"
    data1=pd.read_csv(path_to_csv1, encoding='utf-8')
    data1 = data1.iloc[:,:14]
    merge = data.merge(data1,on='ip_addressport',how='left',suffixes=['_l','_r'])
    merge = merge.fillna(0)
    merge = merge.drop(28,axis=1)
    merge = merge.drop(29,axis=1)
    merge = merge.drop('ip_addressport',axis=1)
    print(merge)
    new_order =[0,1,2,3,4,5,6,7,8,9,'hot','num_failed_login','logged_in','num_compromised','root_shell','su_access','num_root','num_file_creations','num_shells','num_access_files','num_outbound_cmds','is_host_login','is_guest',10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
    df=merge.reindex(columns=new_order)
    print(df)
    df.to_csv(output, header=False,index=False)

def sftp_file_exists(sftp,filename):
    try:
        sftp.get(filename)
        return True
    except FileNotFoundError:
        return False


# Execution Example
sql = 'Select * From demo.kdd_content_features2'
mysqlexportfile = '../extractdata/mysqlexport1.csv'
host = 'localhost'
user = 'user'
password = '12345'
k99featureextract = "/home/monty/Documents/extractdata/outscript.csv"
output = '../mergedata/capturemerged.csv'

myhostname = "192.168.1.20"
myusername = "root"
mypassword = "12345"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
remote_path = "/combind.csv"
flagremotefile = "/flag.file"
flaglocalfile = "/home/monty/Documents/extractdata/flag.file"
while(True):
    runcapture()
    mysql_to_csv(sql, mysqlexportfile, host, user, password)
    mergefilesdata(mysqlexportfile,k99featureextract,output)
    with pysftp.Connection(host=myhostname, username = myusername, password = mypassword, cnopts = cnopts ) as sftp:
        if  not sftp_file_exists(sftp,"flag.file"):    
            sftp.put(output,remote_path)
            sftp.cwd("/")
            sftp.put(flaglocalfile,flagremotefile)
            print("filedropped")
            directory_structure = sftp.listdir_attr()
            for attr in directory_structure:
                print (attr.filename,attr)
        else:
            print("FileMissed") 
