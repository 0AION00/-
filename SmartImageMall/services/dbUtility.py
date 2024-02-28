import pymssql
from services import sysConfig

serverName = sysConfig['dbData']['serverName']
databaseName = sysConfig['dbData']['databaseName']
userName = sysConfig['dbData']['userName']
password = sysConfig['dbData']['password']

def createConnection():
    connect = None
    try:
        connect = pymssql.connect(serverName, userName, password, databaseName)
        print('資料庫連線成功')
        return connect
    except Exception as ex:
        raise ex
    
def update(connect, sqlstr, args):
    try:
        cursor = connect.cursor()
        cursor.execute(sqlstr, args)
        connect.commit()
        return 'seccess!!'
    except Exception as ex:
        connect.rollback()
        raise ex
    
def query(connect, sqlstr, args):
    if connect != None:
        cursor = connect.cursor()
        cursor.execute(sqlstr, args)
        return cursor.fetchone()