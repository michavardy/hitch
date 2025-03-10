import yaml
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich.spinner import Spinner
import subprocess
import shutil
import paramiko

config = yaml.safe_load(Path("hitch.yaml").read_text())
console = Console()

def ssh_run_command_remote_with_progress(command_name: str, remote_host: str, ssh_user: str, password: str, remote_cmd: str, with_output=False) -> None:
    """Runs a command on a remote host via SSH with progress indication using Paramiko."""
    console.print(f"[bold green]Connecting to {remote_host}...[/bold green]")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        with console.status(f"[bold green]Running command on {remote_host}... {command_name}") as status:
            spinner = Spinner("dots12", style="bold yellow")
            status.update(spinner)

            client.connect(remote_host, username=ssh_user, password=password)
            stdin, stdout, stderr = client.exec_command(remote_cmd)

            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                console.print(f"[red]{command_name} failed with error:[/red] {error}")
            else:
                console.print(f"[green]{command_name} completed successfully![/green]")
                if with_output:
                    return output
                console.print(f"[bold cyan]{output}[/bold cyan]")

        client.close()
    except Exception as e:
        console.print(f"[red]Error running command: {str(e)}[/red]")


def scp_transfer_files_to_remote(name: str, local_path: str, remote_host: str, ssh_user: str, password: str, remote_path: str):
    """Transfers files to a remote host via SCP with progress indication using Paramiko."""
    console.print(f"[bold green]Connecting to {remote_host} for SCP...[/bold green]")
    try:
        # Create SSH Client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # <== Fix here
        client.connect(remote_host, username=ssh_user, password=password)

        # Open SFTP Session
        with console.status(f"[bold green]Transferring files to {remote_host}... {name}") as status:
            spinner = Spinner("dots12", style="bold yellow")
            status.update(spinner)
            sftp = client.open_sftp()
            # Ensure remote directory exists
            try:
                sftp.stat(remote_path)  # Check if directory exists
            except FileNotFoundError:
                stdin, stdout, stderr = client.exec_command(f"mkdir -p {remote_path}")

            local_path_obj = Path(local_path)

            if local_path_obj.is_file():
                sftp.put(local_path, f"{remote_path}/{local_path_obj.name}")
            elif local_path_obj.is_dir():
                for file in local_path_obj.glob("**/*"):
                    if file.is_file():
                        remote_file_path = f"{remote_path}/{file.relative_to(local_path)}"
                        sftp.put(str(file), remote_file_path)

            console.print(f"[green]{name} transfer completed successfully![/green]")
            sftp.close()
            client.close()

    except Exception as e:
        console.print(f"[red]Error transferring files: {str(e)}[/red]")


def run_command_with_progress(name:str, cmd:list[str], with_output=False) -> None:
    # Using a single status with spinner for progress
    with console.status(f"[bold green]Running command...{name}") as status:
        # Create a spinner while the process runs
        spinner = Spinner("dots12", style="bold yellow")
        status.update(spinner)  # Updating the spinner into status
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                console.print(f"[green]{name} completed successfully![/green]")
                if with_output:
                    return result.stdout
                else:
                    console.print(f"[bold cyan]{result.stdout}[/bold cyan]")
            else:
                console.print(f"[red]{name} failed with error:[/red] {result.stderr}")
                
        except Exception as e:
            console.print(f"[red]Error running command: {str(e)}[/red]")
            
if __name__ == "__main__":
    #for remote in config.get('remote',[]):
    #    ssh_run_command_remote_with_progress("test_ssh", remote['host'], remote['user'], remote['password'], "ls")
    #for remote in config.get('remote',[]):
    #    scp_transfer_files_to_remote(
    #        name="transfer deploy", 
    #        local_path=config.get('deployment',[]).get("local_directory", "./deploy"), 
    #        remote_host=remote['host'], 
    #        ssh_user=remote['user'], 
    #        password=remote['password'], 
    #        remote_path="/opt/test_hitch")
    pass