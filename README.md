# dice-data-collector

DICE Data Collector Container

This container uses Alpine Linux with Python 3.7.

Current Specs are Flask App running natively.

To get started:

1. Clone the Repo
2. CD into the directory and run docker build -t dice-data-collector .
3. docker run --restart=always --name dice-data-collector -p 80:5000 dice-data-collector

or download the OVA from: 

https://onevmw-my.sharepoint.com/:f:/g/personal/tburge_vmware_com/EnVAcMX3T75Cg3XmJrAOtTUBCBXkKDUrY_QRBRhRZ7XAaQ?e=GZXTdw

TODOs

# Quick

-Change web layer to Gunicorn/nginx

-Add timestamp to filename

-Add property collection for other object types

# Not quick

-Add error checking (Any error comes up as Error 500 currently)

-Add loading screen while appliance is collecting data

-Replicate TDM functionality for vCenter

-Investigate collecting telegraf metrics (Tom)

-Investigate pushing JSON data to API instead of download (Tom)

-Investigate using appliance to push vrops to vCenter (Tom)

# Adds by the team


