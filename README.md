# dice-data-collector

DICE Data Collector Container

This container uses Alpine Linux with Python 3.7.

Current Specs are Flask App running natively.

To get started:

1. Clone the Repo
2. CD into the directory and run docker-compose up --build

or download the OVA from: 

https://onevmw-my.sharepoint.com/:f:/g/personal/tburge_vmware_com/EnVAcMX3T75Cg3XmJrAOtTUBCBXkKDUrY_QRBRhRZ7XAaQ?e=GZXTdw

TODOs

# Tasks

-Add error checking (Any error comes up as Error 500 currently)

-Add Test Connection functionality

-Add Timer for execution

-Replicate TDM functionality for vCenter

-Investigate collecting telegraf metrics (Tom)

-Investigate using appliance to push vrops to vCenter (Tom)

-~~Change web layer to Gunicorn~~

-~~Add timestamp to filename~~

-~~Add property collection for other object types~~

-~~Add loading screen while appliance is collecting data~~

-~~Investigate pushing JSON data to API instead of download~~

# Adds by the team


