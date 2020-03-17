import pymongo
import datetime

import pandas as pd

connection = pymongo.MongoClient(
	host="localhost",
	port=27017
)
db = connection.dn_backup
materia_dn = db.materia_dn

print('--------------------------- Total de materias - ' + str(materia_dn.count_documents({})))

ano_materia = materia_dn.aggregate([
	{
		"$match" : { "dateCreated": {"$lt": datetime.datetime.now()} }
	},
	{
		"$group" : {
			"_id" : { "ano_materia": { "$year" : "$dateCreated" } },
			"count": { "$sum" : 1 }
		}
	},
	{
		"$sort" : { "_id.ano_materia" : -1 }
	}
])

for item in ano_materia:
	if item['_id']['ano_materia'] > 1100:
		print( str(item['_id']['ano_materia']) + ' - ' + str(item['count']))

print('--------------------------- Total de materias - ' + str(materia_dn.count_documents({})))