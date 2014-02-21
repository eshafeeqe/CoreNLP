CoreNLP
=======

Package for process distribution of Standford's CoreNLP 

Dependencies
============

1) pyzmq package: Installation procedure can be found in this link http://zeromq.org/bindings:python

2) CoreNLP python wrapper. Plese visit this link for installation https://bitbucket.org/torotoki/corenlp-python

3) Install mongoDB and pymongo. 

Additional settings for CoreNLP python module
=============================================

a) Set up CoreNLP python wrapper as instructed in the website. 

b) Go to the corenlp folder
	
	cd corenlp

c) Then open the __init__.py file

d) Edit the line 

	from corenlp import batch_parse
	
	as

	from corenlp import batch_parse, parse_parser_results

e) Save the file

d) Go back to the previous folder 

	cd ..

f) Install corenlp modue

	sudo python setup.py install

Running the code
==================

a) Take a terminal and run the client

	python client.py

b) Open the file worker.py and specify the folder path of Standford CoreNLP package

	dir_cornlp = '/media/sda5/test/corenlp-python/stanford-corenlp-full-2014-01-04'

c) Then take another terminal and run worker.py also

	python worker.py

d) Run db_manager.py in another terminal
	
	python db_manager.py


If everything went right, you can see a log file in client folder named main_log.log
which having the information of processing details of articles. 


