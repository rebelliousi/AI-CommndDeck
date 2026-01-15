import socket

def scan_port(port):
    """
    Scan a single port for open status.
    
    Args:
    port (int): The port number to scan.
    
    Returns:
    bool: True if the port is open, False otherwise.
    """
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout of 1 second
        s.settimeout(1)
        
        # Try to connect to the port
        s.connect(('localhost', port))
        
        # If we get here, the port is open
        print(f"Port {port} is open")
        
        # Close the port
        s.close()
        
        return True
    
    except (ConnectionRefusedError, socket.timeout):
        # If we get a connection refused error or the socket times out, the port is closed
        print(f"Port {port} is closed")
        
        return False

def scan_ports(start_port, end_port):
    """
    Scan a range of ports for open status.
    
    Args:
    start_port (int): The start port number.
    end_port (int): The end port number.
    
    Returns:
    list: A list of open ports.
    """
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        # Scan the port
        if scan_port(port):
            # If the port is open, add it to the list
            open_ports.append(port)
    
    return open_ports

def main():
    # Define the range of ports to scan
    start_port = 1
    end_port = 65535
    
    # Scan the ports
    open_ports = scan_ports(start_port, end_port)
    
    # Print the open ports
    if open_ports:
        print("Open Ports:")
        for port in open_ports:
            print(port)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
