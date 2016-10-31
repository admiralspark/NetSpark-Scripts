# NetSpark-Scripts

## What is the purpose?
This repo will hold the cleaned scripts I've made for simplifying repetitive tasks. I'll be making use of Kirk Byers' Netmiko project to hopefully cut down on the work needed to mass-run commands.

## What is the target audience?
Any network administrator who's sick of manually touching things! These are certainly not meant as a replacement for configuration management, NCM, or other products of the like. This is for stuff where we'll be parsing output, making intelligent programmed changes, etc.

## What are the scripts/what do they do?

##### findMAC.py
This script uses the output of "show mac add | inc XXX" where XXX is a manually input mac address. The intent is this: if you have an environment with a dozen switches and you need to find out what port a phone/printer/whatever is plugged into and don't want to check each one by hand, this will pop into each one and spit out what it finds.

EVENTUALLY it will even intelligently tell you which ports are access, which are trunk, and which one is likely the correct port based on collected information.
