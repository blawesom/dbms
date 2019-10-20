#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

from ansible_subprocess import run_playbook

def setup_db(public_ip, engine, name, port, user, password):

    keypair = 'db_manager_key.rsa'
    playbook_file = 'resources/{}.yml'.format(engine)
    setup_vars = {'user': user, 'password': password, 'database': name}
    
    with open('inventory', 'w') as inv:
        inv.write(public_ip)
    
    success, result = run_playbook(playbook_filename=playbook_file, hosts='inventory',
                                    private_key=keypair, extra_vars=setup_vars)#, extra_options='--timeout 60')
    
    if not success:
        if isinstance(result, Exception):
            print(result)
            error, result = result, None
        else:
            print(type(result))
            print(result.__dict__)
            result, error = result, None
    
        return success, result, error
        
    return success, result, None
