import time
import sys
import zmq
from corenlp import *
import datetime

#Initializing corenlp module
dir_cornlp = '/media/sda5/test/corenlp-python/stanford-corenlp-full-2014-01-04'
corenlp = StanfordCoreNLP(dir_cornlp)  # wait a few minutes...
#corenlp2 = StanfordCoreNLP(dir_cornlp)  # wait a few minutes...

print "Now Ready"
#executor = ThreadPoolExecutor(max_workers=1)
# Socket for data recieving from client
context = zmq.Context()
data_recieve = context.socket(zmq.PULL)
data_recieve.connect("tcp://127.0.0.1:5556")

#Socket for acknoldgement to client
control_message = context.socket(zmq.PUSH)
control_message.connect("tcp://127.0.0.1:5557")

#Socket for sending message for saving in to database
db_message = context.socket(zmq.PUSH)
db_message.connect("tcp://127.0.0.1:5558")

poller = zmq.Poller()                                              
poller.register(data_recieve, zmq.POLLIN) 
data_recieve_count = 0   

def message_handling(message):
	"""
	This is the main function for message processing by corenlp module
	"""
	# Some time CoreNLP module gives error due to out of memory
	# then the fuction sleeps for two seconds and try again.	
	try:
		result  = corenlp.raw_parse(message['description'])
	except Exception, e:
		time.sleep(2)
		result  = corenlp.raw_parse(message['description'])
	
	db_data = { "id" : message['id'] , "result" : result }
	print message['id']
	db_message.send_json(db_data)

def transmit_req():
	#print 'transmitting'
	control_message.send("TRANSMIT")

if __name__ == '__main__':    
	#Initial Transmit request

	transmit_req()
	
	while True:
		socks = dict(poller.poll())
	    #  Wait for next request from client
		if data_recieve in socks and socks[data_recieve] == zmq.POLLIN:
			message = data_recieve.recv_json()
			#print 'data_count',data_recieve_count
			if data_recieve_count < 4:
				data_recieve_count = data_recieve_count+1
			else:
				data_recieve_count = 0
				transmit_req()

			message_handling(message)
							

		

 
