# Managed DataBase Service

## Requirements

https://github.com/blawesom/ansible-subprocess
https://github.com/outscale/osc-sdk-python

## Usage

Example:
> python3 service.py

You can create a dbservice through:
> curl -d '{"username":"benjamin", "password":"haxorpassword", "db_name":"mydb"}' -H "Content-Type: application/json" -X POST localhost:8080/api/CreateDB

And describe is different ways:
> curl localhost:8080/api/ReadDB

> curl localhost:8080/api/ReadDB/db-42bd992a

> curl -d '{"service_id":"db-42bd992a"}' -H "Content-Type: application/json" -X POST localhost:8080/api/ReadDB

___options & default value___:

- vmtype: tinav5.c2r4
- storagesize: 100 (in GB)
- storagetype: gp2
- engine: mysql
- port: 3306

## Implementation

### Step 1

- Create VM type
- Choose the allocated storage
- Define name of this DB and Instance
- Define master username of DB
- Define master user password
- Define port for DB

### Step 2

- Choose SQL Engine
- Possibility to choose VPC/Subnet/SG

### Step 3

- Define bucket for backup/daily dump
- Define backup retention period (1 per day)
- Access/Export log

### Step 4

- Activate replicas (bound to available zone)
- Activate encryption
