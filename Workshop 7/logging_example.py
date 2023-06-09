# Caleb St.Germain
# Logging Example
# 03/22/2023
# **Courtesy of Dr. Rahman's workshop7 github repo**

import logging 


def giveMeLoggingObject():
    format_str = '%(asctime)s %(message)s'
    file_name  = 'SIMPLE-LOGGER.log'
    logging.basicConfig(format=format_str, filename=file_name, level=logging.INFO)
    loggerObj = logging.getLogger('simple-logger')
    return loggerObj
