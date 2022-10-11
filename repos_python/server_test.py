import pymssql # mssql import

# 서버 정보
server = '114.31.55.145'
database = 'tjoeun_db'
username = 'tjoeun_user'
password = 'ejwhdms20070815'

####################################################################
# MSSQL 접속
conn = pymssql.connect(server, username, password, database)
# auto commit 사용할 경우 : conn.autocommit(True)
cursor = conn.cursor()
####################################################################

#############################################################################
# SELECT
#query = "SELECT * FROM tjoeun_db.dbo.tj_campus WITH(NOLOCK) WHERE display_yn='Y' "
cursor.execute("SELECT * FROM tjoeun_db.dbo.tj_campus WITH(NOLOCK) WHERE display_yn='Y' ")
row = cursor.fetchone()
while row:
    print(row[0], row[1].encode('ISO-8859-1').decode('euc-kr'))
    row = cursor.fetchone()

# 연결 끊기
conn.close()