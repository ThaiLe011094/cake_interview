def init_logger(name):
    import logging

    try:
        logger = logging.getLogger(name)
        return logger
    except Exception as e:
        return f"No logging for {name} with exception {e}"
