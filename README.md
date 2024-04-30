# LAN-scan

## Usage

To run the script, navigate to the directory containing network_scan.sh and execute it as follows:

```bash
sh nscan.sh  192.168.1.0/24
```

Replace `<subnet>` with the CIDR notation of the subnet you wish to scan, such as `192.168.1.0/24`.

## Output

The script will output a list of active IP addresses within the specified subnet along with their corresponding hostnames, if resolvable. Unresolvable hostnames will be marked as "Unknown".
