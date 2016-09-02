#ATENTION - Export CSV with delimiter of & 

# encoding: utf-8
import csv
import MySQLdb

counter = 1

with open('dump_company.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='&', quotechar='|')
	for row in spamreader:
		insert_string = "insert into vemdolixo_company (organization_name, organization_type, phone, email, city, state, neighborhood, address, website, cnpj, latitude, longitude, is_active) "
		insert_string = insert_string + "values ('" + row[1] + "', '" + row[0] + "', '"+ row[2] +"','" + row[3] + "','" + row[4] + "','" + row[5] + "','" + row[6] + "','" + row[7] + "', '" + row[8] + "', '" + row[9] + "'," + row[10] + "," + row[11] + ", 1 )";
		try:
			# conn = MySQLdb.connect(host= "localhost",
			#                   user="root",
			#                   passwd="root",
			#                   db="vemdolixo")
			conn = MySQLdb.connect(host= "mysql.vemdolixo.com",
			                  user="fafaschiavo",
			                  passwd="310308Fah!",
			                  db="vemdolixo")
			x = conn.cursor()

			x.execute(insert_string)
			conn.commit()
			print 'Success - ' + str(counter)
			counter = counter  + 1
		except Exception, e:
			print row[0]
			print row[1]
			print row[2]
			print row[3]
			print row[4]
			print row[5]
			print row[6]
			print row[7]
			print row[8]
			print row[9]
			print row[10]
			print row[11]
			print 'error - ' + insert_string
			print e

		conn.close()