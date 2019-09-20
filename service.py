#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import flask
import logging
from logging.handlers import RotatingFileHandler

from vm_manager import create_vm
from db_manager import setup_db

SERVICE = { 'name': 'mdbs - managed database service',
            'version': 'alpha 0.1'}

DEFAULT_OPTIONS = { 'profile': 'default',
                    'engine': 'mysql',
                    'port': 3306,
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
# file_handler = RotatingFileHandler('/var/log/mdbs/server_activity.log', 'a', 5000000, 5)
file_handler = RotatingFileHandler('server_activity.log', 'a', 5000000, 5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# flask app
app = flask.Flask(__name__)


def handle_params(payload):
    # Handle mission parameters
    logger.debug('Handling payload: {}'.format(payload))
    if [key for key in MANDATORY_OPTIONS if key not in payload.keys()]:
        missing = [key for key in MANDATORY_OPTIONS if key not in payload.keys()]
        logger.error('Missing parameters: {}'.format(missing))
        flask.abort(400)
        
    else:
        for key in set(list(payload.keys()) + list(DEFAULT_OPTIONS.keys())):
            if key not in payload.keys():
                payload[key] = DEFAULT_OPTIONS[key]
        return payload

@app.route('/api/status', methods=['GET'])
def status():
    return flask.jsonify({  'service': SERVICE,
                            'response': 'service alive'})

@app.route('/api/CreateDB', methods=['POST'])
def CreateDB():
    payload = handle_params(dict(flask.request.form))
    logger.debug('handling request: {}'.format(payload))
    if app.debug == True:
        return flask.jsonify({ 'service': SERVICE,
                                'response': payload
                            })

    success, vm, error = create_vm(profile=payload['profile'], vmtype=payload['vm_type'], 
                                    storage={'type': payload['storage_type'], 'size': payload['storage_size']})

    if success==False:
        print('Infrastructure failed')
        if error:
            return flask.jsonify({  'service': SERVICE,
                                    'response': 'Error -> ' + str(error)})
        else:
            return flask.jsonify({  'service': SERVICE,
                                    'response': 'Error -> Check the vm: {} - {}'.format(vm['VmId'], vm['PublicIp'])})

    success, db, error = setup_db(public_ip=vm['PublicIp'], engine=payload['engine'], name=payload['db_name'],
                                     port=payload['port'], user=payload['user'], password=payload['password'])

    return flask.jsonify({  'service': SERVICE,
                            'response': 'Success -> ' + ':'.join(vm['PublicIp'], payload['port'])})

if __name__ == '__main__':
    # start application to be available from any IP on port 80
    # used only when service.py is directly called
    # all other configuration has been moved to be imported in the package
    app.run(host='127.0.0.1', port=8080, debug=True)