# encoding: utf-8
#ATENTION - Export CSV with delimiter of & 

import csv
import MySQLdb

print 'Hi there!'

conn = MySQLdb.connect(host= "mysql.vemdolixo.com",
              user="fafaschiavo",
              passwd="310308Fah!",
              db="vemdolixo")

x = conn.cursor()

company_id = 1
residue_id = 1
with open('dump_receptivity.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='&', quotechar='|')
	for row in spamreader:
		for match in row:
			if match == 'Sim':
				insert_string = "insert into vemdolixo_receptivity (residue_id, company_id, is_active) values ( " + str(residue_id) + ", " + str(company_id) + ", 1);"
				residue_id = residue_id + 1

				# conn = MySQLdb.connect(host= "localhost",
			 #                  user="root",
			 #                  passwd="root",
			 #                  db="vemdolixo")

				x.execute(insert_string)
				print 'Success - ' + str(company_id)

		residue_id = 1
		company_id = company_id + 1


conn.commit()
conn.close()
# insert into vemdolixo_receptivity (residue_id, company_id, is_active) values (2, 5, 1);