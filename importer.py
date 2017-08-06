#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import MySQLdb

print 'Hi there! lets import some shit'
df = pd.read_excel(open('to_upload.xlsx','rb'), sheetname='PLANILHA VAI TEC FINAL')

residues_to_insert = list(df.columns.values)
residues_to_insert = residues_to_insert[11:]

# db = MySQLdb.connect("localhost","root","root","vemdolixo" )
db = MySQLdb.connect("mysql.vemdolixo.com","fafaschiavo","310308Fah!","vemdolixo" )
cursor = db.cursor()

recently_created_ids = []
for new_residue in residues_to_insert:
	print 'Now inserting - ' + new_residue
	sql = "insert into `vemdolixo_residue`(residue_name, unity) values ('" + new_residue + "', 'Kg');"
	cursor.execute(sql)
	db.commit()
	cursor.execute("select * from vemdolixo_residue order by id desc limit 1;")
	data = cursor.fetchone()
	recently_created_ids.append(data[0])

for index, row in df.iterrows():
	sql = "insert into `vemdolixo_company` (organization_name, organization_type, phone, email, city, state, neighborhood, address, website, cnpj, latitude, longitude, is_active, description, created_at) values ('*LOCAL', 'Cooperativa', '*TELEFONE', '*EMAIL', 'São Paulo', 'São Paulo', '-', '*ENDERECO', '*SITE', '-', *X, *Y, 1, '-', NOW());"
	sql = sql.replace('*LOCAL', row['LOCAL'].encode('utf-8'))
	sql = sql.replace('*TELEFONE', row['TELEFONE'].encode('utf-8'))
	sql = sql.replace('*EMAIL', row['EMAIL'].encode('utf-8'))
	sql = sql.replace('*ENDERECO', row['ENDERECO'].encode('utf-8'))
	sql = sql.replace('*SITE', row['SITE'].encode('utf-8'))
	sql = sql.replace('*X', str(row['X']))
	sql = sql.replace('*Y', str(row['Y']))
	print sql
	cursor.execute(sql)
	db.commit()

	cursor.execute("select * from vemdolixo_company order by id desc limit 1;")
	data = cursor.fetchone()
	current_company_id = data[0]
	line_list = list(row)
	line_list = line_list[-6:]
	print line_list
	print 'Current company id - ' + str(current_company_id)
	print recently_created_ids
	print '-------------'

	index = 0
	for new_residue in recently_created_ids:
		if line_list[index] == 1:
			query = 'insert into vemdolixo_receptivity (residue_id, company_id, minimun, maximun, is_active, created_at) values (*residue_id, *company_id, 0, 0, 1, NOW())'
			query = query.replace('*residue_id', str(new_residue))
			query = query.replace('*company_id', str(current_company_id))
			cursor.execute(query)
			db.commit()
		index = index + 1

db.close()




