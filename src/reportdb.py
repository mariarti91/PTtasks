import sqlite3
import json
import os

def create_empty_db(path):
	"""created empty report db"""
	with sqlite3.connect(path) as db_object:
			cursor = db_object.cursor()
			cursor.execute('CREATE TABLE IF NOT EXISTS control (id TEXT PRIMARY KEY, overview TEXT);')
			cursor.execute('CREATE TABLE IF NOT EXISTS statuses (id INTEGER PRIMARY KEY, value TEXT);')
			cursor.execute("""CREATE TABLE IF NOT EXISTS scandata ( id INTEGER PRIMARY KEY
																  , control_id TEXT
																  , status_id int
																  , FOREIGN KEY(control_id) REFERENCES control(id)
																  , FOREIGN KEY(status_id) REFERENCES statuses(id));""")
			statuses = ['STATUS_COMPLIANT'
					   , 'STATUS_NOT_COMPLIANT'
					   , 'STATUS_NOT_APPLICABLE'
					   , 'STATUS_ERROR'
					   , 'STATUS_EXCEPTION']

			statuses = [ [statuses.index(i) + 1, i] for i in statuses]
			cursor.executemany("INSERT INTO statuses VALUES (?, ?);", statuses)



class ReportDataBase():
	"""class for working with report database"""
	def __init__(self, path='report.db'):
		self.path = path

		if not os.path.isfile(self.path):
			create_empty_db(self.path)

		with sqlite3.connect(self.path) as db_object:
			cursor = db_object.cursor()
			cursor.execute("PRAGMA foreign_keys = ON;")
			with open('controls.json', 'r') as f:
				controls = json.load(f)
			try:
				cursor.executemany("INSERT INTO control VALUES (?, ?);", controls)
			except Exception as e:
				print(str(e))

	def add_control(self, id_, status):
		"""insert data into scandata table"""
		with sqlite3.connect(self.path) as db_object:
			cursor = db_object.cursor()
			cursor.execute("PRAGMA foreign_keys = ON;")
			cursor.execute("INSERT INTO scandata (control_id, status_id) VALUES (?, ?);", (id_, status))

	def get_scandata(self):
		"""get information from scandata table"""
		with sqlite3.connect(self.path) as db_object:
			cursor = db_object.cursor()
			cursor.execute("""SELECT control.id, control.overview, statuses.value
							  FROM scandata
							  INNER JOIN control ON scandata.control_id=control.id
							  INNER JOIN statuses ON statuses.id=scandata.status_id;""")
			return cursor.fetchall()



_reportdb = ReportDataBase()

def add_control(id_, status, db=_reportdb):
	db.add_control(id_, status)

def get_scandata(db=_reportdb):
	return db.get_scandata()