#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import sys, os
import zmq
import logging
from logging.handlers import RotatingFileHandler

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBService, Base, entry_exists, create_entry

from db_manager import setup_db

# logger declaration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# configure log file to rotate in 5 files of 5MB
file_handler = RotatingFileHandler('dbworker_activity.log', 'a', 5000000, 5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.debug('Log started...')

# zmq queue setup
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind('tcp://*:5555')

# local service db
engine = create_engine('sqlite:///dbms.db')
if not os.path.isfile('dbms.db'):
    sys.exit()

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    while True:
        message = socket.recv_json()
        logger.debug('handling request: {}'.format(message))
        # http://zguide.zeromq.org/py:all#Divide-and-Conquer
        
        # launch ansible config
        # setup_db
        # manage db writting depending on output
        logger.debug('job done')
        
        socket.send(b"True")

