import sys
import socket
import argparse
import logging
import concurrent.futures
from datetime import datetime

def setup_logging(log_file="port_scanner.log"):
    # Create a custom logger
    logger = logging.getLogger("PortScanner")
    logger.setLevel(logging.DEBUG)
    # Create handlers: console and file
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_file)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)
    # Create formatters and add them to handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger

# ANSI color codes
GREEN = "\033[92m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"
# Code block style: super light grey background with black text
CODEBLOCK = "\033[48;5;250m\033[38;5;0m"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Python Port Scanner: A concurrent port scanning tool for production use."
    )
    parser.add_argument(
        "target",
        help="Target hostname or IP address"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start of port range (default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=9999,
        help="End of port range (default: 9999)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Timeout for each port in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=500,
        help="Number of concurrent threads (default: 500)"
    )
    parser.add_argument(
        "--log",
        type=str,
        default="port_scanner.log",
        help="Log file name (default: port_scanner.log)"
    )
    return parser.parse_args()

def resolve_target(target, logger):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror as e:
        logger.error(f"Unable to resolve hostname '{target}': {e}")
        sys.exit(1)

def scan_port(target, port, timeout, logger):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except Exception as e:
        logger.debug(f"Error scanning port {port}: {e}")
    return None

def main():
    args = parse_args()
    logger = setup_logging(args.log)
    logger.info("Starting Python Port Scanner in production mode.")

    target_ip = resolve_target(args.target, logger)

    header = f"""
{BLUE}########################{RESET}
{BLUE}# {GREEN}Python Port Scanner {RESET}{BLUE} # {RESET}
{BLUE}########################{RESET}

{BLUE}Scan Target:{RESET} {target_ip}
{BLUE}Scanning started:{RESET} {datetime.now()}
{BLUE}Port Range:{RESET} {args.start} - {args.end}
{BLUE}Timeout:{RESET} {args.timeout} sec per port
{BLUE}Workers:{RESET} {args.workers}
"""
    print(header)
    logger.info("Scan parameters established, commencing port scan...")

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(scan_port, target_ip, port, args.timeout, logger): port
                   for port in range(args.start, args.end + 1)}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                result = future.result()
                if result is not None:
                    print(f"{BLUE}Port number {result} is open{RESET}")
                    open_ports.append(result)
            except Exception as e:
                logger.error(f"Error scanning port {port}: {e}")

    logger.info("Port scan complete.")
    logger.info(f"Open ports: {open_ports}")
    print(f"\n{BLUE}Scan complete. Open ports: {open_ports}{RESET}")
    sys.exit(0)

if __name__ == '__main__':
    main()

