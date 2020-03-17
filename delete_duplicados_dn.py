import pymongo
import datetime

import pandas as pd
import logging
from bson import ObjectId

connection = pymongo.MongoClient(
	host="localhost",
	port=27017
)
db = connection.dn_backup
materia = db.materia_dn

logger = logging.getLogger("mylogger")

for mat in materia.aggregate([
		{
			'$group': {
				'_id': "$id_dn",
				'count':{'$sum': 1}
			}
		},
		{
			'$match': { 'count': {'$gt': 1}}
		}
	]):
	logger.warning(mat)

	for m in materia.find(
		{
			'id_dn': mat['_id']
		}):
		if('link' in m):
			logger.warning(m['link'])
		else:
			logger.warning('APAGAR O ' + str(m['_id']))
			
			materia.delete_one( {"_id": ObjectId(m['_id'])});