import yaml
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from hitch.commands.command import run_command_with_progress, scp_transfer_files_to_remote, ssh_run_command_remote_with_progress
import shutil

config = yaml.safe_load(Path("hitch.yaml").read_text())

def copy_resources():
    local_deployment_directory = config.get('deployment',[]).get("local_directory", "./deploy")
    Path(local_deployment_directory).mkdir(exist_ok=True)
    deployment_resources = config.get("deployment",[]).get("resources", [])
    for resource in deployment_resources:
        shutil.copy(resource, local_deployment_directory)
        
def transfer_deployment_to_remote():
    for remote in config.get('remote',[]):
        scp_transfer_files_to_remote(
            name="transfer deploy", 
            local_path=config.get('deployment',[]).get("local_directory", "./deploy"), 
            remote_host=remote['host'], 
            ssh_user=remote['user'], 
            password=remote['password'], 
            remote_path=config.get("deployment",[]).get('remote_directory',"/opt"))

def execute_install_commands():
    for remote in config.get('remote',[]):
        for command in config.get("deployment",[]).get("install_command",[]):
            ssh_run_command_remote_with_progress("deployment_command", remote['host'], remote['user'], remote['password'], command)

def execute_cleanup_commands():
    for remote in config.get('remote',[]):
        for command in config.get("deployment",[]).get("cleanup_commands",[]):
            ssh_run_command_remote_with_progress("deployment_command", remote['host'], remote['user'], remote['password'], command)

def main():
    copy_resources()


if __name__ == "__main__":
    main()