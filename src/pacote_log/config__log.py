import logging


def configurar_logger(nome_logger='app', arquivo_log='app.log', nivel=logging.INFO):

    logger = logging.getLogger(nome_logger)
    logger.setLevel(nivel)

    formatador = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Cria e configura o manipulador de console
    manipulador_console = logging.StreamHandler()
    manipulador_console.setFormatter(formatador)
    logger.addHandler(manipulador_console)

    # Se o arquivo de log for fornecido, cria e configura o manipulador de arquivo
    if arquivo_log:
        manipulador_arquivo = logging.FileHandler(arquivo_log)
        manipulador_arquivo.setFormatter(formatador)
        logger.addHandler(manipulador_arquivo)

    return logger
