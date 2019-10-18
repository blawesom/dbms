#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import sys, os
import time
import argparse
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

# local service db
engine = create_engine('sqlite:///dbms.db')
if not os.path.isfile('dbms.db'):
    sys.exit()

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', dest='public_ip', type=str, help='public IP to join the VM')
    parser.add_argument('-eng', dest='engine', type=str, help='SQL engine, mysql or posgre')
    parser.add_argument('-db', dest='name', type=str, help='SQL Database name to create') #posgre or mysql
    parser.add_argument('-port', dest='port', type=int ,help='port on which the engine will be exposed')
    parser.add_argument('-user', dest='user', type=str, help='master username')
    parser.add_argument('-pass', dest='password', type=str, help='master password')
    
    config = vars(parser.parse_args())

    #time.sleep(60)
    success, result, error = setup_db(**config)

    db = session.query(DBService).filter_by(public_ip=config['public_ip']).first()

    if error:
        logger.error(error)
        db.state = 'error'
    if success:
        logger.info(result)
        db.state = 'available'
    session.commit()
    