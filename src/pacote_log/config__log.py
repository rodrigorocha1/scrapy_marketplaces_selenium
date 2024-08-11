import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler('teste.log')
fh.setLevel(logging.INFO)


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s'
)


ch.setFormatter(formatter)
fh.setFormatter(formatter)


logger.addHandler(ch)
logger.addHandler(fh)
