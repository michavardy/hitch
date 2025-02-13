import typer
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from hitch.commands.image import build_images, build_tar_files
from hitch.commands.deployment import copy_resources, transfer_deployment_to_remote, execute_install_commands, execute_cleanup_commands
from hitch.commands import ssh_tunnel
from rich import print
from sshtunnel import SSHTunnelForwarder


app = typer.Typer()

@app.command()
def build():
    build_images()
    build_tar_files()

@app.command()
def deploy():
    copy_resources()
    transfer_deployment_to_remote()
    execute_install_commands()

@app.command()
def cleanup_deployment():
    execute_cleanup_commands()

@app.command()
def connect_ssh_tunnel():
    ssh_tunnel.connect_ssh_tunnel()

@app.command()
def remove_ssh_tunnel():
    ssh_tunnel.remove_ssh_tunnel()

@app.command()
def up():
    print("up")

@app.command()
def down():
    print("down")






if __name__ == "__main__":
    app()