import psycopg2
import time
import inspect
from datetime import datetime

class Connector:
    
    psqlConnection = None
    psqlCursor = None

    @classmethod
    def Connect(cls):  
        try:
            cls.psqlConnection = psycopg2.connect(
                dbname='postgres', 
                user='postgres', 
                host='localhost', 
                password='odoo'
            )
            print("Connected to PostgreSQL")
            cls.psqlCursor = cls.psqlConnection.cursor()

        except:
            print("Unable to connect to database.")
    
    @classmethod
    def Disconnect(cls):
        if cls.psqlConnection is not None:
            cls.psqlCursor.close()
            cls.psqlConnection.close()
            print("Disconnected from PostgreSQL")
    
    @classmethod
    def Insert(cls, f_name, py_name, t_s, t_d, is_f):
        insert_query = "INSERT INTO function_call(function_name, py_file_name, time_stamp, time_date, is_first) VALUES(%s, %s, %s, %s, %s);"
        cls.psqlCursor.execute(insert_query, (f_name, py_name, t_s, t_d, is_f))
        cls.psqlConnection.commit()
    
    @classmethod
    def Select(cls):
        select_query = "SELECT * FROM function_call;"
        cls.psqlCursor.execute(select_query)
        function_call_records = cls.psqlCursor.fetchall()
        return function_call_records

def function_info(func):
    
    def wrapper(*args, **kwargs):
        Connector.Connect()
        func_name = func.__name__
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        py_file_name = module.__file__
        print(py_file_name)
        timeStamp = time.ctime()
        LocalDateTime = datetime.now()
        LocalDateTimeStr = LocalDateTime.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        first_call = True
        table_records = Connector.Select()
        for record in table_records:
            if record[0]==func_name:
                first_call=False
                break
        Connector.Insert(func_name, py_file_name, timeStamp, LocalDateTimeStr, first_call)
        func()
        Connector.Disconnect()
    return wrapper

if __name__ == '__main__':

    pass

    # @function_info
    # def test_function():
    #     print("I'm testing right now.")

    # test_function()