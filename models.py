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
    db_engine = Column(String)
    vm_id = Column(String)
    public_ip = Column(String)
    service_id = Column(String)
    public_port = Column(Integer)
    state = Column(String, default='pending')
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def entry_exists(session, service_id):
    if session.query(DBService).filter_by(service_id=service_id).first():
        return True
    return False


def create_entry(session, vm_id, public_ip, service_id, public_port, db_engine):
    if not entry_exists(session, service_id):
        new_service = DBService(vm_id=vm_id, public_ip=public_ip, service_id=service_id, public_port=int(public_port), db_engine=db_engine)
        session.add(new_service)
        session.commit()
        return True
    else:
        return False


def delete_entry(session, service_id):
    if entry_exists(session, service_id):
        to_delete = session.query(DBService).filter_by(service_id=service_id).first()
        session.delete(to_delete)
        session.commit()
        return True
    return False
