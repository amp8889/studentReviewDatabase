import os
import paramiko
import time

def create_ssh_tunnel(local_port, remote_host, remote_port, ssh_host, ssh_port, ssh_username, ssh_key_path):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SSH server using an SSH key
    ssh_client.connect(ssh_host, ssh_port, ssh_username, key_filename=ssh_key_path)

    # Create an SSH tunnel
    transport = ssh_client.get_transport()
    tunnel = transport.open_channel(
        'direct-tcpip',
        (remote_host, remote_port),
        ('', local_port)
    )

    # Print a message to indicate the tunnel is ready
    print(f"SSH tunnel established on local port {local_port}")

    # Return the SSH client, transport, and tunnel so they can be closed later
    return ssh_client, transport, tunnel

if __name__ == '__main__':
    # SSH server details
    ssh_host = '44.192.127.235'  # Replace with your EC2 instance's public IP or DNS
    ssh_port = 22  # Default SSH port
    ssh_username = 'ec2-user'  # SSH username
    private_key_file = 'private-subnet.pem'
    private_key_path = os.path.join(os.path.dirname(__file__), private_key_file)

    ssh_key_path = private_key_path    # Path to your private key file

    # Remote resource details
    remote_host = 'database.ckceiladqgeo.us-east-1.rds.amazonaws.com'  # RDS endpoint
    remote_port = 3306  # RDS port

    # Local port for the tunnel
    local_port = 3306  # Use the same local port as the one you used in PowerShell

    # Create and maintain the SSH tunnel until the user interrupts the script
    ssh_client, transport, tunnel = create_ssh_tunnel(local_port, remote_host, remote_port, ssh_host, ssh_port, ssh_username, ssh_key_path)

    try:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
            print("Closing the SSH tunnel...")
    finally:
            # Close the SSH tunnel, tunnel, and the SSH client
            tunnel.close()
            transport.close()
            ssh_client.close()
