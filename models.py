#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'benjamin.laplane'

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DBService(Base):
    __tablename__ = 'db_services'
    id = Column(Integer, primary_key=True)
    sqlite_autoincrement = True
    vm_id = Column(String)
    public_ip = Column(String)
    service_id = Column(String)
    public_port = Column(Integer)
    state = Column(String, default='pending')


def entry_exists(session, service_id)
    if session.query(Service).filter_by(service_id=service_id).first():
        return True
    return False


def create_entry(session, vm_id, public_ip, service_id, public_port):
    if not entry_exists(session, service_id):
        new_service = DBService(vm_id, public_ip, service_id, public_port)
        session.add(new_service)
        session.commit()
        return True
    else:
        return True
