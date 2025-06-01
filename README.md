# Find Roku Devices using python3

This script discovers DIAL-compatible devices (including Roku) on the local network using SSDP.

Sends M-SEARCH request to discover UPnP devices
Filters responses for DIAL devices (looking for /dial/dd.xml endpoints)
Retrieves and parses device XML to extract friendly names

Usage: python3 roku.py
