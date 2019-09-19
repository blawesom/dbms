#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import json
import flask
import datetime
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
file_handler = RotatingFileHandler('/var/log/mdbs/server_activity.log', 'a', 5000000, 5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# flask app
app = flask.Flask(__name__)

def handle_params(payload):
    # Handle mission parameters
    if None in [value for key,value in payload.items() if key in MANDATORY_OPTIONS]:
        return flask.jsonify({  'service': SERVICE,
                                'response': 'Missing parameter: {}'.format('/'.join([key for key,value in payload.items() if value==None]))})
        #  flask.abort(400)    # missing arguments
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
    payload = handle_params(flask.request.json())        

    success, vm, error = create_vm(profile=payload['profile'], vmtype=payload['vm_type'], 
                                    storage={'type': payload['storage_type'], 'size': payload['storage_size']})

    if success==False:
        print('Infrastructure failed')
        if error:
            return flask.jsonify({  'service': SERVICE,
                                    'response': 'Error -> ' + str(error))})
        else:
            return flask.jsonify({  'service': SERVICE,
                                    'response': 'Error -> Check the vm: {} - {}'.format(vm['VmId'], vm['PublicIp'])})

    success, db, error = setup_db(public_ip=vm['PublicIp'], engine=payload['engine'], name=payload['db_name'],
                                     port=payload['port'], user=payload['user'], password=payload['password'])

    return flask.jsonify({  'service': SERVICE,
                            'response': 'Success -> ' + ':'.join(vm['PublicIp'], args.port)

if __name__ == '__main__':
    # start application to be available from any IP on port 80
    # used only when server.py is directly called
    # all other configuration has been moved to be imported in the package
    app.run(host='127.0.0.1', port=8080)