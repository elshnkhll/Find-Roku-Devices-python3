import socket
import time
import re
import urllib.request
import xml.etree.ElementTree as ET

# M-SEARCH request
msearch_request = '\r\n'.join([
    'M-SEARCH * HTTP/1.1',
    'HOST: 239.255.255.250:1900',
    'MAN: "ssdp:discover"',
    'MX: 2',
    'ST: ssdp:all',
    '', ''
]).encode('utf-8')

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(5)

# Send M-SEARCH
sock.sendto(msearch_request, ('239.255.255.250', 1900))
print("M-SEARCH sent. Waiting for /dial/dd.xml responses...\n")

locations = set()
start = time.time()

while True:
    try:
        data, addr = sock.recvfrom(1024)
        text = data.decode('utf-8', errors='replace')
        match = re.search(r'(?i)^location:\s*(.+)$', text, re.MULTILINE)
        if match:
            location = match.group(1).strip()
            if location.endswith("/dial/dd.xml") and location not in locations:
                locations.add(location)
                print(f"{addr[0]}: {location}")
                
                # Try to fetch and parse the XML
                try:
                    with urllib.request.urlopen(location, timeout=3) as response:
                        xml_data = response.read()
                        tree = ET.fromstring(xml_data)

                        # Handle namespaces
                        ns = {'upnp': 'urn:schemas-upnp-org:device-1-0'}
                        fname = tree.find('.//upnp:friendlyName', ns)
                        if fname is not None:
                            print(f"  ↳ friendlyName: {fname.text}")
                        else:
                            print("  ↳ friendlyName not found")
                except Exception as e:
                    print(f"  ↳ Failed to fetch/parse XML: {e}")
    except socket.timeout:
        break
    if time.time() - start > 5:
        break

sock.close()
