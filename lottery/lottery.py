import sys
import sqlite3
from sqlite3 import Error
import datetime
from random import randrange

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def create_candidate(conn, candidate):
	sql = ''' insert into candidate(id_no,plate_no,apply_dt,batch,prize_id) values(?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, candidate)
	conn.commit()
	return cur.lastrowid

def update_candidates(conn, candidates):
	sql = ''' update candidate set apply_dt = ? , batch = ? , prize_id = ? WHERE id_no = ? and plate_no = ? '''
	cur = conn.cursor()
	cur.executemany(sql, ((candidate[2], candidate[3], candidate[4], candidate[0], candidate[1]) for candidate in candidates))
	print("affected rows " + str(cur.rowcount))
	conn.commit()

def select_non_prized_candiate(conn):
	sql = ''' select * from candidate where apply_dt is null '''
	cur = conn.cursor()
	cur.execute(sql)
	return cur.fetchall()

def select_non_prized_cnt(conn):
	sql = ''' select count(*) from candidate where apply_dt is null '''
	cur = conn.cursor()
	cur.execute(sql)
	return cur.fetchone()[0]

def batch_in_today_existed(conn, today_str, batch):
	sql = ''' select count(*) from candidate where apply_dt = ? and batch = ? '''
	cur = conn.cursor()
	cur.execute(sql, (today_str, batch))
	if cur.fetchone()[0] > 0:
		return True
	return False
		
batch_detail = ((1,1),(2,5),(3,10))

def main():
	today=datetime.date.today()
	today_str = today.strftime('%Y-%m-%d')
	print("本日為 " + today_str)

	batch = int(input("請輸入批次號:"))
		
	database = "candidate.sqlite"	
	conn = create_connection(database)
	
	with conn:
		# 檢查此批次號是否已經存在
		if batch_in_today_existed(conn, today_str, batch):
			print("此批次號已存在....!!")
			sys.exit()
			
		# 取出所有未中獎過的候選名單
		candidates = select_non_prized_candiate(conn)
		count_candidates = select_non_prized_cnt(conn)
		print("候選名單總數為 " + str(count_candidates), flush = True)
		
		# 中獎者的清單
		winner_keys = []
		winners = []
				
		for detail in batch_detail:
			cnt = 0
			while cnt < detail[1]:
				# 隨機從候選名單挑一個
				idx = randrange(count_candidates)

				# 取得證號車號
				id_no = candidates[idx][0]
				plate_no = candidates[idx][1]
				
				# 判斷此證號車號是否已在中獎清單
				if (id_no, plate_no) in winner_keys:
					continue
				else:
					cnt = cnt + 1
					winner_keys.append((id_no, plate_no))
					winners.append((id_no, plate_no, today, batch, detail[0]))
		
		# 將中獎者更新至資料庫
		update_candidates(conn, winners)

if __name__ == '__main__':
	main()
