from sshtunnel import SSHTunnelForwarder
import yaml
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
import multiprocessing
import os
import signal

config = yaml.safe_load(Path("hitch.yaml").read_text())
TUNNEL_PID_FILE = "ssh_tunnel_pids.txt"  # File to store PIDs

def open_ssh_tunnel(ssh_host:str, ssh_user:str, ssh_password:str, remote_port:int, local_port:int) -> None:
    try:
        print(f"Trying to start tunnel: {ssh_host}:{remote_port} -> localhost:{local_port}")
        with SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                local_bind_address=('127.0.0.1', local_port),
                remote_bind_address=('127.0.0.1', remote_port)) as server:
            server.start()
            print(f"SSH tunnel established: localhost:{local_port} -> {ssh_host}:{remote_port}")
    except:
        print("Connection Failed")
        breakpoint()

def connect_ssh_tunnel() -> list[SSHTunnelForwarder]:
    processes = []
    for remote in config.get('remote',[]):
        for tunnel in config.get("ssh_tunnels",[]):
            process = multiprocessing.Process(
                target=open_ssh_tunnel,
                args=(remote['host'], remote['user'], remote['password'], tunnel['remote_port'], tunnel['local_port']),
                daemon=True
            )
            process.start()
            processes.append(process.pid)
    with open(TUNNEL_PID_FILE, "w") as f:
        for pid in processes:
            f.write(str(pid) + "\n")
    breakpoint()
def remove_ssh_tunnel():
    """Stops all running SSH tunnels by killing their PIDs."""
    if not os.path.exists(TUNNEL_PID_FILE):
        print("No SSH tunnels are currently running.")
        return

    with open(TUNNEL_PID_FILE, "r") as f:
        pids = [int(line.strip()) for line in f.readlines()]

    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Stopped SSH tunnel (PID {pid})")
        except ProcessLookupError:
            print(f"Process {pid} not found.")

    os.remove(TUNNEL_PID_FILE)
    print("All SSH tunnels stopped.")
    
if __name__ == '__main__':
    connect_ssh_tunnel()

        