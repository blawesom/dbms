# Homemade RDS-like

## Prereqs

Install osc-sdk-python and prepare credentials

## Usage

Example:
> python3 main.py --engine mysql --db mydb --user benjamin --password haxorpassword

___options & default value___:

- vmtype: tinav4.c2r4
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
