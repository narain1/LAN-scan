import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
import psutil

def get_hostname_by_ip(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        # return "Hostname could not be resolved"
        pass
    except socket.gaierror:
        # return "Hostname could not be resolved (DNS resolution failure)"
        pass

async def get_hostname_async(ip_address, executor):
    loop = asyncio.get_running_loop()
    # Run the blocking function using the thread pool
    hostname = await loop.run_in_executor(executor, get_hostname_by_ip, ip_address)
    return hostname

async def process_ip_range(base_ip, start, end, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [get_hostname_async(f"{base_ip}.{i}", executor) for i in range(start, end + 1)]
        results = await asyncio.gather(*tasks)
        for ip, hostname in zip([f"{base_ip}.{i}" for i in range(start, end + 1)], results):
            if hostname != None: print(ip, hostname)

def get_wifi_ip_address():
    # Get all network interface addresses
    interfaces = psutil.net_if_addrs()
    for interface_name, addrs in interfaces.items():
        # Identify WiFi interfaces typically named like 'Wi-Fi', 'wlan0', etc.
        if 'wi-fi' in interface_name.lower() or 'wlan' in interface_name.lower():
            for addr in addrs:
                # Check for IPv4 addresses (ignore IPv6 and other types)
                if addr.family == socket.AF_INET:
                    return addr.address
    return "No WiFi interface found or it doesn't have an IPv4 address assigned."


async def main(wifi_ip):
    base_ip = '.'.join(wifi_ip.split('.')[:-1])
    # Example: parallelize with up to 100 workers
    await process_ip_range(base_ip, 1, 1024, 100)

wifi_ip = get_wifi_ip_address()
asyncio.run(main(wifi_ip))
