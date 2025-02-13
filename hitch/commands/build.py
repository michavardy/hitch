import typer
import subprocess
import requests
import os

app = typer.Typer()

SYNCTHING_URL = "https://github.com/syncthing/syncthing/releases/latest/download/syncthing-linux-amd64.tar.gz"

def download_syncthing():
    typer.echo("Downloading Syncthing...")
    response = requests.get(SYNCTHING_URL, stream=True)
    with open("syncthing.tar.gz", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    typer.echo("Syncthing downloaded.")

def build_docker_image():
    typer.echo("Building Docker image...")
    subprocess.run(["docker", "build", "-t", "hitch-image", "."], check=True)
    subprocess.run(["docker", "save", "-o", "hitch-image.tar", "hitch-image"], check=True)
    typer.echo("Docker image saved as hitch-image.tar.")

@app.command()
def run():
    download_syncthing()
    build_docker_image()
    typer.echo("Build completed.")

