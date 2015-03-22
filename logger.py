import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.logThreads = 0
logging.basicConfig(filename="xmp.log", 
		    format='%(levelname)s:%(asctime)s.%(msecs)d:%(funcName)s:%(lineno)d:%(message)s',
		    datefmt="%H:%M:%S",
                    level=logging.DEBUG)