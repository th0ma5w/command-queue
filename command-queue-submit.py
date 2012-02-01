#!/usr/bin/python
import xmlrpclib, logging, sys

# configuration
HOSTCONFIGURATION = 'http://localhost:8020'
ENVIRONMENT = "DEV"
LOGLEVEL = logging.INFO
PARAMETERVALUE=""

# logging configuration
logging.basicConfig(level=LOGLEVEL, format=ENVIRONMENT + ' %(asctime)s %(levelname)s: %(message)s')

try:
        # get the parameter value to submit from the command line
        PARAMETERVALUE = sys.argv[1]
        logging.debug(repr((PARAMETERVALUE, HOSTCONFIGURATION)))
        s = xmlrpclib.ServerProxy(HOSTCONFIGURATION)
        logging.info("Submitting: %s" % PARAMETERVALUE)
        result = s.add_job(PARAMETERVALUE)
        logging.info("Submitted: %s (%s)" % (PARAMETERVALUE, result))
except:
        logging.error("There was an error submitting: %s" % PARAMETERVALUE)



