import zmq,json
from corenlp import parse_parser_results
from pymongo import MongoClient, Connection
import datetime

 

context = zmq.Context()
db_data = context.socket(zmq.PULL)

try:
	db_data.bind("tcp://127.0.0.1:5558")
except Exception, e:
	db_data.connect("tcp://127.0.0.1:5558")


poller = zmq.Poller()                                              
poller.register(db_data, zmq.POLLIN)

logger = context.socket(zmq.PUSH)
logger.connect("tcp://127.0.0.1:5559")


client = MongoClient('localhost', 27017)
db = client['test-database']
articles = db.articles

def db_write(db_message):
	"""fuction for writing corenlp result to db"""

	parsed_dict = parse_parser_results(db_message["result"])
	write_to_db = {"Article_id":db_message["id"],"corenlp_output":parsed_dict ,"date": datetime.datetime.utcnow()}
	article_id = articles.insert(write_to_db)
	log_message = "Article id:" + str(db_message["id"]) + " processed with corenlp at time: " + str(datetime.datetime.utcnow())
	#print log_message
	logger.send(log_message)



if __name__ == '__main__':
	#pool = Pool(processes=5)    
	while True:
		socks = dict(poller.poll())
	  	if db_data in socks and socks[db_data] == zmq.POLLIN:
	  		db_message = db_data.recv_json()
	  		#pool.apply_async(db_write, db_message)
	  		db_write(db_message)
