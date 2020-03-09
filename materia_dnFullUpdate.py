import pymongo
import datetime

connection = pymongo.MongoClient(
	host="localhost",
	port=27017
)
db = connection.dn_backup
materia_dn = db.materia_dn


for materia in materia_dn.find():
	if isinstance(materia['id_dn'], str):
		dateCreated = datetime.datetime.strptime(materia['dateCreated'], "%Y-%m-%d %H:%M:%S")

		data = {
			'dateCreated': dateCreated,
			'link_rel': int(materia['link_rel']),
			'link_rel_interno': int(materia['link_rel_interno']),
			'id_dn': int(materia['id_dn'])
		}

		print("Materia DN " + str(materia['id_dn']))


		materia_dn.update_one(
			{
				'id_dn': materia['id_dn']
			},
			{"$set":data}, True
		)

	print("DN " + str(materia['id_dn']))