import zmq
import sys, os
import time
import json
from  multiprocessing import Process
import logging

data_count = 0

def message_handling():

    """
    This is the main process which send article content to the workers.
    When ever worker become ready after some initialization time, it send a 
    message to the client, then this process start by sending ten (configurable number) 
    messages of article data. The worker process start working and if 
    it processed five articles, then an acknologment has been provided 
    by worker in respond to that client sends five more to the worker socket.
    By which we are maintaining a stable and rush free client server communication.
    """
    #Reading JSON dump
    json_data=open('article_dump.json')
    data = json.load(json_data)
    json_data.close()

    context = zmq.Context()
    START = True
    
    #print "Connecting to server..."
    #Socket for Sending artilce content
    data_sent = context.socket(zmq.PUSH)
    data_sent.bind("tcp://127.0.0.1:5556")

    #Socket for Recieving acknoldgement from worker process
    control = context.socket(zmq.PULL)
    control.bind("tcp://127.0.0.1:5557")

    #Poller for acknologment messages from worker process
    poller = zmq.Poller()                                              
    poller.register(control, zmq.POLLIN) 

    def message_transmit (number_of_msgs):
        """
        This fuction responsible for sending each article data towards worker process
        """

        global data_count
        for reqnum in range(number_of_msgs):
            work_message = { "id" : data_count , "description" : data[data_count]['description'] }
            data_count = data_count+1 
            data_sent.send_json(work_message)


    #Polling happening here
    while True:
        socks = dict(poller.poll())
        if control in socks and socks[control] == zmq.POLLIN:
            #print 'poll breaks'
            control_data = control.recv()
            if control_data == "TRANSMIT":
                #print "control recieved"
                if START == True :
                    message_transmit(10)
                    START = False
                else:
                    message_transmit(5)
def logger():
    """
    The main process responsible for loggging
    Other worker and db process can connect with this logger throgh socket

    """
    print "starting logger"
    log_file = os.path.abspath('manin_log.log')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')
    #Logger Socker
    context = zmq.Context()
    central_logger = context.socket(zmq.PULL)
    central_logger.bind("tcp://127.0.0.1:5559")
    
    #Poller Object for logger Socket
    poller = zmq.Poller()                                              
    poller.register(central_logger, zmq.POLLIN) 

    while True :
        socks = dict(poller.poll())
        if central_logger in socks and socks[central_logger] == zmq.POLLIN:

            log_message = central_logger.recv()
            #print log_message
            logging.info(log_message)
    
if __name__ == '__main__':    
    
    #The main process just turing on the two processors one for message handling
    #Second for the Log Handling
    Process(target = message_handling, args=()).start()
    Process(target = logger, args = () ).start()


