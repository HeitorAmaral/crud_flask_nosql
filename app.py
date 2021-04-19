"""
Executable file.
"""
import os
import logging
from src import app

os.environ['WERKZEUG_RUN_MAIN'] = 'true'
logging.basicConfig(filename="logFile.log", level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(levelname)s %(name)s %('
                           'threadName)s: %(message)s')
log = logging.getLogger('werkzeug')
log.disabled = True


if __name__ == '__main__':
    app.run(host='0.0.0.0')
