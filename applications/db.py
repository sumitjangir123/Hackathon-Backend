import pyodbc
server = 'hackathon-challenge3-team5.database.windows.net'
database = 'Team5challenge3'
username = "adminTeam5"
password = 'h@ck@th0n'   
driver= '{ODBC Driver 17 for SQL Server}'

def upload_data():
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ANALYTICS_DATA
                (DIVISION, COLOR, PRODUCT_TYPE,
                RESULT_SET)
                VALUES (?, ?, ?,?)
                """,
                ("men",'red' , 'shirt', 'temp')
            )
       
