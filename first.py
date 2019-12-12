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
        insert_query = "INSERT INTO function_call(function_name, "\
                                                "py_file_name, "\
                                                "time_stamp, "\
                                                "time_date, "\
                                                "is_first) "\
                        "VALUES(%s, %s, %s, %s, %s);"
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
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        py_file_name = module.__file__
        first_call = True
        for record in Connector.Select():
            if record[0]==func.__name__:
                first_call=False
                break
        Connector.Insert(func.__name__,
                        py_file_name, time.ctime(),
                        datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                        first_call)
        func()
        Connector.Disconnect()
    return wrapper

if __name__ == '__main__':
    pass
    # @function_info
    # def test_function():
    #     print("TESTING.")
    #
    # test_function()
