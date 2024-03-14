import mysql.connector as msc
from dotenv import load_dotenv
import os


class DatabaseOverlay:
    _cursor = None
    _con = None

    def __init__(self):
        load_dotenv()  
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT")
        self.user = os.getenv("MYSQL_USER")
        self.passwd = os.getenv("MYSQL_PASS")
        self.database = os.getenv("MYSQL_DB")
        self._con = None
        self._cursor = None

    def get_connect(self):
        """
        Create or get a MySQL connection object
        In the case of an exception, we check the different known errors
        :return: The connection object.
        """
        try:
            self._con = msc.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                auth_plugin='mysql_native_password'
            )
            if self._con.is_connected():
                print("Connected to MySQL database")
            return self._con

        except msc.Error as e:
            print("Error while connecting to MySQL", e)
            return None

    def get_cursor(self):
        """
        The get_cursor function creates a cursor object for the database connection
        :return: A cursor object.
        """
        if self._con is None or not self._con.is_connected():
            self._con = self.get_connect()

        self._cursor = self._con.cursor(buffered=True)
        return self._cursor

    def getCurrentID(self, table, ID="ID"):
        """
        # SQL
        SELECT max(ID) from table;

        # Python
        def getCurrentID(self, table, ID="ID"):
                cursor = self.get_cursor()
                query = "SELECT max(ID) from {};".format(table)
                cursor.execute(query)
                id = cursor.fetchone()[0]
                if self.verbose:print("query selected: ", query, " " + " id inserted : ", id )
                return id

        # The above function is a simple function that returns the maximum ID in a table.
        #
        # The function is called in the following manner:
        #
        #

        :param table: the name of the table you want to insert into
        :param ID: the name of the column that you want to use as the ID, defaults to ID (optional)
        :return: The last ID in the table.
        """
        cursor = self.get_cursor()
        query = "SELECT max("+ID+") from {};".format(table)
        cursor.execute(query)
        id = cursor.fetchone()[0]
        print("query selected: ", query, " " + " id inserted : ", id )
        return id

    def next_id(self, table, ID="ID"):
        """
        Given a table name and an ID, return the next ID in sequence

        :param table: the name of the table to be queried
        :param ID: The name of the ID column in the table, defaults to ID (optional)
        :return: The next ID number for the table.
        """
        new_id = self.getCurrentID(table, ID) + 1
        print("New ID (table : ",table, ") : ", new_id)
        return str(new_id)

    def insert(self, table, innerSql, ID="ID"):
        """
        This function inserts a new row into a specified table with a given inner SQL statement and returns the ID of the
        new row.

        :param table: The name of the table where the data will be inserted
        :param innerSql: The SQL statement to be executed as part of the insert query. It contains the values to be inserted
        into the table
        :param ID: The default value for the primary key column of the table. If not specified, it assumes the column name
        is "ID", defaults to ID (optional)
        :return: the value of `idx`, which is the ID of the newly inserted row in the specified table.
        """
        idx = self.next_id(table, ID)
        sql = "insert into "+table+" values("+idx+","+innerSql+");"
        print(sql)
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
        except msc.Error as e:
            msg = "Error sql ("+sql+") = "+str(e.errno)+" : "+e.msg
            print(msg)
            return -1
        self.commit()
        return idx

    def query(self, sql):
        cursor = self.get_cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        return data

    def close(self):
        if self._con:
            self._con.close()

    def commit(self):
        if self._con:
            self._con.commit()

    def is_closed(self):
        return self._con is None or not self._con.is_connected()

    def update(self, table :str, set :str, where:str) -> bool:
        sql = "update "+table+" set "+set+" where "+where+";"
        print(sql)
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
        except msc.Error as e:
            msg = "Error sql ("+sql+") = "+str(e.errno)+" : "+e.msg
            print(msg)
            return False
        self.commit()
        return True

    def get_con(self):
        """
        Returns the connection object
        :return: The connection object.
        """
        return self._con