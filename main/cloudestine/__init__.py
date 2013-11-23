import logging
import logging.config

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',level=logging.DEBUG)
gnupg_logger=logging.getLogger("gnupg").setLevel(logging.INFO)