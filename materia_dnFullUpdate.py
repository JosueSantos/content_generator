import pymongo
import datetime
from bson import ObjectId

connection = pymongo.MongoClient(
	host="localhost",
	port=27017
)
db = connection.dn_backup
materia_dn = db.materia_dn


for materia in materia_dn.find(no_cursor_timeout=True):
	if isinstance(materia['id_dn'], str):
		dateCreated = datetime.datetime.strptime(materia['dateCreated'], "%Y-%m-%d %H:%M:%S")

		id_dn = materia['id_dn']
		if ('/' in materia['id_dn']):
			id_dn = materia['id_dn'].split('1.')[-1]

		data = {
			'dateCreated': dateCreated,
			'link_rel': int(materia['link_rel']),
			'link_rel_interno': int(materia['link_rel_interno']),
			'id_dn': int(id_dn)
		}

		print("Materia DN " + str(materia['id_dn']))


		materia_dn.update_one(
			{
				"_id": ObjectId(materia['_id'])
			},
			{"$set":data}, True
		)

	print("DN " + str(materia['id_dn']))