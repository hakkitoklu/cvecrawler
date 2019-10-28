import mysql
from mysql.connector import Error

class db():
    def insert(cveid, cweid, vul_type, p_date, u_date, score, access, info):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='cve',
                                                 user='root',
                                                 password='')

            cursor = connection.cursor()
            sql = "INSERT INTO data (cveid,cweid,vul_type,p_date,u_date,score,access,info) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (cveid, cweid, vul_type, p_date, u_date, score, access, info,)
            cursor.execute(sql, val)
            connection.commit()
            print("Record inserted successfully into data table")

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")