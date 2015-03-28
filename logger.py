import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.logThreads = 0
logging.basicConfig(filename="/dev/stderr",
		    format='%(levelname)s: %(asctime)s.%(msecs)d: %(filename)s:%(lineno)d:  %(funcName)s: %(message)s',
		    datefmt="%H:%M:%S",
                    level=logging.DEBUG)
