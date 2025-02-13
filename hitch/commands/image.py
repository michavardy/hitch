import yaml
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
from hitch.commands.command import run_command_with_progress
import shutil

config = yaml.safe_load(Path("hitch.yaml").read_text())

def build_images():
    for image in config['images']:
        if "dockerfile_path" in image.keys():
            cmd = ["docker", "build", "-t", f"{image['name']}:{image['tag']}", image['dockerfile_path']]
            run_command_with_progress("build_local_image",cmd)
        else:
            cmd = ["docker", "pull", image['image']]
            run_command_with_progress("pull_remote_image",cmd)
            
def parse_output(output:str) -> dict:
    parsed = []
    for index, line in enumerate(output.split('\n')):
        if not line:
            continue
        if index == 0:
            headers = line.split()
        if index != 0:
            parsed.append(dict(zip(headers, line.split())))
    return parsed
            
def build_tar_files():
    local_deployment_directory = config.get("local_deployment_directory", "./deploy")
    Path(local_deployment_directory).mkdir(exist_ok=True)
    for image in config['images']:
        image_name = f"{image['name']}"
        image_output = run_command_with_progress(f"check_image_{image_name}", ["docker","images", image_name], with_output=True)
        parsed = parse_output(image_output)
        if parsed:
            run_command_with_progress(f"build_{image_name}_tar", ["docker","save", '-o', f"{image_name}.tar", image_name])
            shutil.move(f"./{image_name}.tar", local_deployment_directory)   
            
def main():
    #build_images()
    build_tar_files()


if __name__ == "__main__":
    main()