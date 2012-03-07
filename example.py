import logging
from HttpServedHandler import HttpServedHandler
import time


def fizzbuzz(value):
    if value % 5 == 0 and value % 3 == 0:
        logging.error('%d fizzbuzz' % value)
    elif value % 5 == 0:
        logging.warn('%d buzz' % value)
    elif value % 3 == 0:
        logging.warn('%d fizz' % value)
    else:
        logging.info('%d' % value)


if __name__ == '__main__':
    formatting = logging.Formatter('%(asctime)s %(name)s:%(threadName)s\t%(levelname)s\t%(message)s')
    logging.getLogger('').setLevel(logging.NOTSET)
    c = logging.StreamHandler()
    c.setLevel(logging.INFO)
    c.setFormatter(formatting)
    logging.getLogger('').addHandler(c)

    h = HttpServedHandler(9876)
    h.setLevel(logging.NOTSET)
    h.setFormatter(formatting)
    logging.getLogger('').addHandler(h)


    logging.info('Starting Example')
    for x in range(100):
        fizzbuzz(x)
    logging.warn('You have 10 seconds to see the log in a web browser before I exit!')
    time.sleep(10)


    

