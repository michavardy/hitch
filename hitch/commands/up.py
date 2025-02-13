import typer
import paramiko
from hitch.commands.syncthing import setup_syncthing
from hitch.commands.deploy import deploy_k8s

app = typer.Typer()

REMOTE_HOST = "your-remote-host"
SSH_USER = "your-user"
SSH_KEY = "/path/to/ssh-key"

def ssh_connect():
    typer.echo(f"Connecting to {REMOTE_HOST} via SSH...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(REMOTE_HOST, username=SSH_USER, key_filename=SSH_KEY)
    return client

@app.command()
def run():
    ssh_client = ssh_connect()
    deploy_k8s(ssh_client)
    setup_syncthing(ssh_client)
    typer.echo("Remote environment set up.")

