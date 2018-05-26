import subprocess
import re


class ConnectedDevicesScanner:
    NMAP_SCAN_COMMAND = ["nmap", "-sn", "192.168.0.0/24"]
    ARP_SCAN_COMMAND = ["arp-scan", "-l"]

    def __init__(self):
        self.scan_command = self.NMAP_SCAN_COMMAND
        self._mac_pattern = re.compile(r'(?:[0-9a-fA-F]:?){12}')

    @classmethod
    def from_nmap(cls):
        obj = cls()
        obj.scan_command = cls.NMAP_SCAN_COMMAND
        return obj

    @classmethod
    def from_arp_scan(cls):
        obj = cls()
        obj.scan_command = cls.ARP_SCAN_COMMAND
        return obj

    def find_connected_device_macs(self):
        out = subprocess.check_output(self.scan_command)
        mac_addrs = re.findall(self._mac_pattern, out.decode("utf8"))
        mac_addrs = [x.lower() for x in mac_addrs]
        return mac_addrs
