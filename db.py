import sqlite3

dbname = "users.db"

def CreateTable():

	con = sqlite3.connect(dbname)
	cur = con.cursor()


	cur.execute("""CREATE TABLE IF NOT EXISTS users(
					id int,
					flag int
	)""")

	con.close()

def FindFlag(tgchatid):

	con = sqlite3.connect(dbname)
	cur = con.cursor()

	cur.execute("SELECT flag FROM users WHERE id=?", (tgchatid))
	result = cur.fetchone()

	con.commit()
	con.close()
	return result[0]

def AddUser(tgchatid):
	con = sqlite3.connect(dbname)
	cur = con.cursor()

	cur.execute("INSERT INTO users VALUES (?, ?) ", (tgchatid, 0))

	con.commit()
	con.close()

def Flag0(tgchatid):
	con = sqlite3.connect(dbname)
	cur = con.cursor()

	cur.execute("UPDATE users SET flag = ? WHERE id = ?", (0, tgchatid))

	con.commit()
	con.close()

def Flag1(tgchatid):
	con = sqlite3.connect(dbname)
	cur = con.cursor()

	cur.execute("UPDATE users SET flag = ? WHERE id = ?", (1, tgchatid))

	con.commit()
	con.close()