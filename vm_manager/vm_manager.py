#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import json
import time
from osc_sdk_python import Gateway

TIMEOUT=60

def create_vm(profile, vmtype, storage):
    gw = Gateway(**{'profile': profile})
    
    with open('/Users/benjaminlaplane/.oapi_credentials') as creds:
        credentials = json.load(creds)
        region = credentials[profile]['region']
    with open('config/omi.json') as omis:
        omi_list = json.load(omis)
        image = omi_list[region]
    try:
        if 'db_manager_key' not in [key['KeypairName'] for key in gw.ReadKeypairs()['Keypairs']] :
            new_keypair = gw.CreateKeypair(KeypairName='db_manager_key')
            with open('../db_manager_key.rsa', 'w') as newkey:
                newkey.write(new_keypair['Keypair']['PrivateKey'])

        new_vm = gw.CreateVms(ImageId=image, VmType=vmtype, KeypairName='db_manager_key')['Vms'][0]
        new_vol = gw.CreateVolume(Size=storage['size'], VolumeType=storage['type'], SubregionName=region + 'a')

        #new_eip = gw.CreatePublicIp()
        #gw.LinkPublicIp(VmId=new_vm['Vms'][0]['VmId'], PublicIp=new_eip['PublicIp']['PublicIp'])

        gw.LinkVolume(VmId=new_vm['VmId'], VolumeId=new_vol['Volume']['VolumeId'], DeviceName='/dev/xvdb')
    except Exception as errorExcept:
        return False, None, errorExcept

    new_vm = gw.ReadVms(Filters={'VmIds': [new_vm['VmId']]})['Vms'][0]

    if waitforit(gw=gw, vms=[new_vm], state='running'):
        return True, new_vm, None
    return False, new_vm, None


def waitforit(gw, vms, state):
    waited = 0
    while waited < TIMEOUT:
        req_vm_list = gw.ReadVmsState(AllVms=True, Filters={'VmIds': [vm['VmId'] for vm in vms]})
        vm_list = req_vm_list['VmStates']
        # print('\nRequestId: {}\n Result: {}\n'.format(req_vm_list['ResponseContext']['RequestId'], vm_list))

        if not vm_list:
            return False
        if len([vm for vm in vm_list if vm['VmState'] != state]):
            # print('waiting for: {} ({})'.format(vm_list, waited))
            time.sleep(1)
            waited +=1
        else:
            return True
    return False
