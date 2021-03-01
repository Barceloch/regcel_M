#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
# PROJECT   : RegCEl - Registro para el Consumo Eléctrico                                              #
# VERSION   : 1.2                                                                                                      #
# AUTHOR    : Yunior Barceló Chávez             barceloch@gmail.com                                                                         #
# DATE      : 9/01/2021                                                                                               #
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
from utils import app_data_dir
from sqlite3 import Error
import sqlite3
import os

class Database:
    # Insert into database
    def insert_into_database(self, tableName, conn, data):

        if conn is not None:
            try:
                c = conn.execute("select * from {}".format(tableName))
                fields = tuple([des[0] for des in c.description][:])

                if "id" in fields:
                    fields = tuple(list(fields)[1:])
                cur = conn.cursor()
                cur.execute(
                    """
					INSERT INTO {}
					{} VALUES {}
					""".format(
                        tableName, fields, data
                    )
                )
                conn.commit()
                return True
            except Error as e:
                pass
        return None

    # Update Database
    def update_database(self, tableName, conn, fields, field_vals, ref, index):
        if conn is not None:
            try:
                cur = conn.cursor()
                if not isinstance(fields, tuple) and not isinstance(fields, list):
                    fields = list([fields])
                    field_vals = list([field_vals])

                for field, field_val in zip(fields, field_vals):
                    # print(field,field_val)
                    cur.execute(
                        """
							UPDATE {}
							SET {}= ? WHERE {}= ?
							""".format(
                            tableName, field, ref
                        ),
                        (field_val, index),
                    )
                conn.commit()
                return True
            except Exception as e:
                pass
                # print("Error in updating data: {}".format(e))
        return None

    # Delete from Database
    def delete_from_database(self, tableName, conn, condition):
        if conn is not None:
            try:
                cur = conn.cursor()
                # just to track if deletion was successful
                count = len(
                    cur.execute(
                        """
						SELECT * FROM {} WHERE {}
						""".format(
                            tableName, condition
                        )
                    ).fetchall()
                )
                if not count:
                    return False
                cur.execute(
                    """
						DELETE FROM {} WHERE {}
						""".format(
                        tableName, condition
                    )
                )
                conn.commit()
                return True
            except Error as e:
                pass
                # print("Error in deleting data: {}".format(e))
        return False

    # Search in the database
    def search_from_database(self, tableName, conn, prop, value, order_by="reg"):
        if conn is not None:
            try:
                cur = conn.cursor()
                # print("cur: {}".format(cur))
                filtered_list = cur.execute(
                    """
							SELECT * FROM {} WHERE {} LIKE ? ORDER BY {};
						""".format(
                        tableName, prop, order_by
                    ),
                    (str(value) + "%",),
                ).fetchall()
                return filtered_list
            except Error as e:
                pass
                # print("Error in searching: {}".format(e))

        return None

    def search_from_database_many(self, tableName, conn, condition):
        if conn is not None:
            try:
                cur = conn.cursor()
                filtered_list = cur.execute(
                    """
						SELECT * FROM {} WHERE {}
						""".format(
                        tableName, condition
                    )
                ).fetchall()
                return filtered_list
            except Error as e:
                pass
                # print("Error in deleting data: {}".format(e))
        return None

    # connect database
    def connect_database(self, db_file):
        try:
            conn = sqlite3.connect(app_data_dir()+"/.regceldb/" + db_file)
            return conn

        except Error as e:
            pass

        return None

    # create table
    def create_table(self, table, conn):

        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(table)
            except Error as e:
                pass
                
            conn.commit()

    def delete_table(self, db_file, table_name):
        conn = self.connect_database(db_file)
        if conn is not None:
            cur = conn.cursor()
            try:
                cur.execute("DROP TABLE {}".format(table_name))
                conn.commit()
                conn.close()
                return True
            except:
                return False

    def findTables(self, db_file):
        conn = self.connect_database(db_file)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [each[0] for each in cur.fetchall()]
        # conn.close()

    def addData(self, db_file, table, tableName, data):

        table = table.format(tableName)
        conn = self.connect_database(db_file)

        if conn is not None:
            self.create_table(table, conn)
            tmp = self.insert_into_database(tableName, conn, data)
            conn.close()
            return tmp
        return None

    def extractAllData(self, db_file, tableName, order_by="reg"):
        conn = self.connect_database(db_file)

        if conn is not None:
            cur = conn.execute(
                "SELECT * FROM {} ORDER BY {}".format(tableName, order_by)
            )
            data = cur.fetchall()
            conn.close()
            return data
        return None

    def delete_all_data(self, db_file, tableName):
        conn = self.connect_database(db_file)

        if conn is not None:
            # conn.commit()
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM {};
                """.format(
                    tableName
                )
            )
            conn.commit()
            conn.close()


