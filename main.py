#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import sys
import argparse
from vm_manager import create_vm
from db_manager import setup_db

DEFAULT_OPTIONS = { 'profile': 'default',
                    'engine': 'mysql',
                    'port': 3306,
                    'vm_type': 'tinav5.c2r4',
                    'stor_type': 'gp2',
                    'stor_size': 100
                }
MANDATORY_OPTIONS = ['db_name', 'user', 'password']

def main(args):
    # Handle mission parameters
    if None in [value for key,value in vars(args).items() if key in MANDATORY_OPTIONS]:
        print('Missing parameter: \n - {}'.format('\n - '.join([key for key,value in vars(args).items() if value==None])))
        sys.exit()

    vm_id = create_vm(profile=args.profile, vmtype=args.vm_type, storage={'type': args.stor_type, 'size': args.stor_size})

    if vm_id==False:
        print('VM not ready, check it: {}'.format(vm_id))
        sys.exit()

    db = setup_db(public_ip=ip, engine=args.engine, name=args.db_name, port=args.port, user=args.user, password=args.password)
    
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-api', dest='profile', help='oapi credentials profile', default=DEFAULT_OPTIONS['profile'])
    parser.add_argument('-eng',dest='engine', type=str, help='SQL engine, mysql or posgre', default=DEFAULT_OPTIONS['engine'])
    parser.add_argument('-db', dest='db_name', type=str, help='SQL Database name to create')
    parser.add_argument('-port', dest='port', type=int ,help='port on which the engine will be exposed', default=DEFAULT_OPTIONS['port'])
    parser.add_argument('-user', dest='user', type=str, help='master username')
    parser.add_argument('-pass', dest='password', type=str, help='master password')
    parser.add_argument('-vm', dest='vm_type', type=str, help='vm type', default=DEFAULT_OPTIONS['vm_type'])
    parser.add_argument('-type', dest='stor_type', type=str, help='storage type', default=DEFAULT_OPTIONS['stor_type'])
    parser.add_argument('-size', dest='stor_size', type=int, help='storage size', default=DEFAULT_OPTIONS['stor_size'])

    main(parser.parse_args())
