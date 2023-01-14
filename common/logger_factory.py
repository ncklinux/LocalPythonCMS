import logging


class LoggerFactory(object):
    @staticmethod
    def createLogger(name):
        fileFormatter = logging.Formatter(
            "%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s"
        )
        consoleFormatter = logging.Formatter("%(levelname)s -- %(message)s")

        fileHandler = logging.FileHandler("logs/logdata.log")
        fileHandler.setLevel(logging.WARN)
        fileHandler.setFormatter(fileFormatter)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(consoleFormatter)

        logger = logging.getLogger(name)
        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)
        logger.setLevel(logging.DEBUG)

        return logger
