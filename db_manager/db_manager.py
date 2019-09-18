#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'


# help
# https://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api
# Check Saltstack call from python program
# Check existing salt pillars ?

# import ansible.runner

def setup_db(public_ip, engine, name, port, user, password):
    print('installing {}'.format(engine))
    return True
