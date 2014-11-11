# -*- coding: utf-8 -*-

import time
import math
import sys



from pymongo import Connection

db = Connection()

mongo_test = db.test_db.test_collection

mongo_test.remove()


sys.stdout = open('stats.html', 'w')
print "<style>td { font: 12px Verdana; }</style>"
print "<table>"



def report(txt):
	per_sec = (float(cnt) / (time.clock()-start_time)) / 1000
	color = 'red' if 'mongo' in txt.lower() else 'blue'
	color = 'green' if 'inno' in txt.lower() else color
	print "<tr><td>%35s<td>%5.1fK per sec<td><div style='background:%s; width:%dpx;'>&nbsp;</div>" % (txt, per_sec, color, int(math.log(per_sec)/math.log(1.02)))


for cnt in (250, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000):

	mongo_test.remove()
	print '<tr><td><br><br><b>', cnt, 'items</b>'



	# MONGO INSERT
	start_time = time.clock()

	for i in xrange(cnt):
		i1 = str(i+1)
		mongo_test.insert({'_id': i1, 'value': i1})
	report('Mongo INSERTs')
	print



	# MONGO SELECT
	start_time = time.clock()
	for i in xrange(cnt):
		i1 = str(i+1)
		obj = mongo_test.find({'_id': i1})[0]['value']
		assert(obj == i1)
	report('Mongo SELECTs')

	print
