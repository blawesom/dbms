#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = 'Benjamin'

import os
import json
from osc_sdk_python import Gateway

TIMEOUT=60

def create_vm(profile, vmtype, storage):
    gw = Gateway(**{'profile': profile})
    
    # print(os.path.dirname(os.path.abspath(__file__)))
    
    with open('/Users/benjaminlaplane/.oapi_credentials') as creds:
        credentials = json.load(creds)
        region = credentials[profile]['region']
    with open('resources/omi.json') as omis:
        omi_list = json.load(omis)
        image = omi_list[region]

    new_vm = gw.CreateVms(ImageId=image, VmType=vmtype)
    new_vol = gw.CreateVolume(Size=storage['size'], VolumeType=storage['type'], SubregionName=region + 'a')
    #new_eip = gw.CreatePublicIp()
    
    #gw.LinkPublicIp(VmId=new_vm['Vms'][0]['VmId'], PublicIp=new_eip['PublicIp']['PublicIp'])
    gw.LinkVolume(VmId=new_vm['Vms'][0]['VmId'], VolumeId=new_vol['Volume']['VolumeId'], DeviceName='/dev/xvdb')

    if waitforit(gw, [new_vm['Vms'][0]['VmId']], 'running'):
        return new_vm['Vms'][0]['VmId']#, new_eip['PublicIp']['PublicIp']
    return False#, new_eip['PublicIp']['PublicIp']

def waitforit(gw, vmids, state):
    waited = 0
    while waited < TIMEOUT:
        if not ['Fail' for vmid in vmids if gw.ReadVmsState(vmid)['VmStates'][0]['VmState'] != state]:
            waited +=1
        else:
            return True
    return False