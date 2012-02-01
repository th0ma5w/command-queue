#!/usr/bin/python
import threading, datetime, Queue, logging
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from time import sleep
from subprocess import Popen, PIPE

# configuration
HOSTCONFIGURATION = ("localhost", 8020)
ENVIRONMENT = "DEV"
LOGLEVEL = logging.INFO
SCRIPTCOMMAND = "/bin/echo" #example or for testing


# logging configuration
logging.basicConfig(level=LOGLEVEL, format=ENVIRONMENT + ' %(asctime)s %(levelname)s: %(message)s')
logging.info("Server will now start.")


# Initialize the queue
q=Queue.Queue()
logging.debug("Queue created.")

#a counter since restart
COUNTER = 0

def add_job(job_name):
        """add an entry to the queue"""
        global COUNTER
        q.put(job_name)
        message = "Successfully queued: #%s - %s " % (COUNTER, job_name)
        logging.info(message)
        COUNTER += 1
        return message

def run_job(job_name):
        """actually execute the work"""
        logging.info("Running job: %s" % job_name)
        output = ''
        try:
                cmd = [SCRIPTCOMMAND, job_name]
                logging.debug("Executing: %s" % (' '.join(cmd)))
                process = Popen(cmd,stdout=PIPE,stderr=PIPE,stdin=PIPE)
                output = process.communicate()
                logging.debug("The command executed properly.")
        except:
                logging.error("The command did not execute properly.")
        logging.debug(repr((cmd,output)))

class JobRunner(threading.Thread):
        """thread that waits forever with 10 second sleep time the execute items one at a time from the queue spaced by 2 seconds"""
        LOOP=True
        def run(self):
                while self.LOOP:
                        qsize = q.qsize()
                        if qsize > 0:
                                run_job(q.get())
                                qsize -= 1
                                logging.debug("Waiting for 2 seconds before checking the queue again. Current queue size is %s." % qsize)
                                sleep(2)
                        else:
                                logging.debug("Queue is empty. Sleeping for 10 seconds before checking the queue again.")
                                sleep(10)

# instantiate the thread, make it a daemon, and start
t = JobRunner()
t.daemon = True
t.start()
logging.debug("Queue monitor thread started.")

# setup the XMLRPC server
class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

# start the server
try:
        server = SimpleXMLRPCServer(HOSTCONFIGURATION, requestHandler=RequestHandler)
except:
        logging.error("Error binding to port")
        logging.info("Sending kill to threads...")
        t.LOOP = False

try:
        server.register_introspection_functions()
        # register the queue adding function with the XMLRPC server
        server.register_function(add_job)
except:
        pass

try:
        server.serve_forever()
except:
        logging.info("Sending kill to threads...")
        t.LOOP = False


