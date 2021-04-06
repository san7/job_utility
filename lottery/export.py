import sqlite3
from sqlite3 import Error
import datetime
import csv

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def select_prized_candiate(conn, apply_dt, batch):
	sql = ''' select * from candidate where apply_dt = ? and batch = ? order by prize_id '''
	cur = conn.cursor()
	cur.execute(sql, (apply_dt, batch))
	return cur.fetchall()
	
def main():
	year = int(input("請輸入抽獎日期年:"))
	month = int(input("請輸入抽獎日期月:"))
	day = int(input("請輸入抽獎日期日:"))
	date1 = datetime.date(year, month, day)
	batch = int(input("請輸入批次號:"))

	database = "candidate.sqlite"	
	conn = create_connection(database)
	
	with conn:
		candidates = select_prized_candiate(conn, date1, batch)
		for candidate in candidates:
			print(candidate)

	with open('output.csv', 'w', newline='') as myfile:
		wr = csv.writer(myfile)
		wr.writerow(['證號','車號','抽獎日期','批次','獎項'])
		wr.writerows(candidates)
	
if __name__ == '__main__':
	main()
