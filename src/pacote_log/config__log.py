import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


file_handler = logging.FileHandler('web_scraping.log', encoding='utf-8')
file_handler.setLevel(logging.ERROR)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)


formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adiciona os handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
