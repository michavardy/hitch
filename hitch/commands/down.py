import typer
import subprocess

app = typer.Typer()

@app.command()
def run():
    typer.echo("Tearing down environment...")
    subprocess.run(["kubectl", "delete", "-f", "deployment.yaml"], check=True)
    subprocess.run(["kubectl", "delete", "-f", "service.yaml"], check=True)
    typer.echo("Cleanup complete.")
