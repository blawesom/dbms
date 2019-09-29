#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import os
import logging
from logging.handlers import RotatingFileHandler
import secrets
import flask
import zmq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBService, Base, entry_exists, create_entry
from vm_manager import create_vm

SERVICE = { 'name': 'mdbs - managed database service',
            'version': 'alpha 0.1'}

DEFAULT_OPTIONS = { 'profile': 'default',
                    'engine': 'mysql',
                    'port': 3306, #5432 for posgre
                    'vm_type': 'tinav5.c2r4',
                    'storage_type': 'gp2',
                    'storage_size': 100
                }

MANDATORY_OPTIONS = ['db_name', 'username', 'password']

# logger declaration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# configure log file to rotate in 5 files of 5MB
file_handler = RotatingFileHandler('dbms_activity.log', 'a', 5000000, 5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# local service db
engine = create_engine('sqlite:///dbms.db')
if not os.path.isfile('dbms.db'):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# flask app
app = flask.Flask(__name__)


def handle_params(payload):
    # Handle mission parameters
    logger.debug('Handling payload: {}'.format(payload))
    if [key for key in MANDATORY_OPTIONS if key not in payload.keys()]:
        missing = [key for key in MANDATORY_OPTIONS if key not in payload.keys()]
        logger.error('Missing parameters: {}'.format(missing))
        flask.abort(400, description="Required parameter is missing")
    else:
        for key in set(list(payload.keys()) + list(DEFAULT_OPTIONS.keys())):
            if key not in payload.keys():
                payload[key] = DEFAULT_OPTIONS[key]
        return payload


def register_new_service(vm_id, vm_ip, vm_port):
    service_id = 'db-{}'.format(secrets.token_hex(4))
    while entry_exists(session=session, service_id=service_id):
        service_id = 'db-{}'.format(secrets.token_hex(4))
        logger.info('Managing service creation: {}'.format(service_id))
    if create_entry(session=session, vm_id=vm_id, public_ip=vm_ip, service_id=service_id, public_port=vm_port, engine=payload['engine']):
        return service_id
    else:
        flask.abort(400, description="Error when creating service")


@app.route('/api', methods=['GET'], strict_slashes=False)
def status():
    return flask.jsonify({  'service': SERVICE })


@app.route('/api/CreateDB', methods=['POST'])
def create_db():
    payload = handle_params(dict(flask.request.json))
    logger.debug('handling request: {}'.format(payload))

    success, vm, error = create_vm(profile=payload['profile'], vmtype=payload['vm_type'],
                                    storage={'type': payload['storage_type'], 'size': payload['storage_size']})

    if error:
        flask.abort(400, description=str(error))
    if not success:
        return flask.jsonify({'service': SERVICE,
                              'response': 'unsuccessful operation'})
        
    payload['vm_ip'] = vm['Nics'][0]['LinkPublicIp']['PublicIp']
    payload['vm_id'] = vm['VmId']
    payload['service_id'] = register_new_service(vm_id=payload['vm_id'], vm_ip=payload['vm_ip'], vm_port=payload['port'])

    # fork setup of VM to queue

    return flask.jsonify({'service': SERVICE,
                          'response': {
                          'db': {'Public_Ip': payload['vm_ip'],
                                 'Public_Port': payload['port'],
                                 'Service_Id': payload['service_id'],
                                 'State': 'pending'}}})


@app.route('/api/ReadDB', methods=['GET, POST'])
@app.route('/api/ReadDB/<service_id>', methods=['GET'])
def get_db(service_id=None):
    payload={}
    if flask.request.method == 'POST':
        service_id = flask.request.json.get(service_id, None)

    if service_id:
        return flask.jsonify({'service': SERVICE,
                              'response': session.query(DBService).filter_by(service_id=service_id).all()})
    
    return flask.jsonify({'service': SERVICE,
                          'response': session.query(DBService).all()})


if __name__ == '__main__':
    logger.debug(str(app.url_map))
    app.run(host='127.0.0.1', port=8080, debug=True)
    