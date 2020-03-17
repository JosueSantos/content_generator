import pymongo
import datetime

import pandas as pd
from bson import ObjectId

connection = pymongo.MongoClient(
	host="localhost",
	port=27017
)
db = connection.dn_backup
materia = db.materia_dn

id_materias = [
	2024597,
	2016962,
	1872632
]

for mat in materia.find(
	{
		'id_dn': { '$in':id_materias }
	},
	{'id_dn':1, 'titulo':1, 'dateCreated':1}
	):
	print('----------------------------')
	print(mat)