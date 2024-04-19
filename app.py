from io import BytesIO
import os
import base64
import sys
import subprocess
from PIL import Image
import re
import json
from urllib import request
import requests
import subprocess

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

OUTPUT_DIR = "/var/nfs-mount/Passion-ComfyUI-Volumes/output"
INPUT_DIR = "/var/nfs-mount/Passion-ComfyUI-Volumes/input"
HELPER_DIR = "/var/nfs-mount/Passion-ComfyUI-Volumes/helpers"
COMFYUI_TEMP_OUTPUT_DIR = "/tmp"

print("OUTPUT_DIR: ", OUTPUT_DIR)
print("INPUT_DIR: ", INPUT_DIR)
print("HELPER_DIR: ", HELPER_DIR)
print("COMFYUI_TEMP_OUTPUT_DIR: ", COMFYUI_TEMP_OUTPUT_DIR)

sys.path.insert(1, os.path.join(__location__, "./ComfyUI"))
sys.path.insert(1, HELPER_DIR)

import subprocess

def list_directory_contents():
    try:
        output = subprocess.check_output(['ls'], universal_newlines=True)
        print("Directory contents:")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Failed to list directory contents: {e}")
    try:
        output = subprocess.check_output([f"ls {os.path.join(__location__, "./ComfyUI")}"], universal_newlines=True)
        print("Directory contents:")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Failed to list directory contents: {e}")
    try:
        output = subprocess.check_output([f"ls {os.path.join(__location__, "./ComfyUI/helpers")}"], universal_newlines=True)
        print("Directory contents:")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Failed to list directory contents: {e}")

list_directory_contents()

from helpers.comfyui import ComfyUI

class InferlessPythonModel:
    @staticmethod
    def convert_image_to_base64(image_path):
        with Image.open(image_path) as image:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()

    @staticmethod
    def process_single_image(image_path):
        try:
            base64_image = InferlessPythonModel.convert_image_to_base64(image_path)
            # os.remove(image_path)  # Delete the image after conversion
            return base64_image
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return e
        
    @staticmethod
    def get_final_image_name(directory):
        pattern = re.compile(r"ComfyUI_(\d+)_\.png$")
        max_number = 0

        print("*******************************", flush=True)
        for filename in os.listdir(directory):
            print("FileName: ", filename, flush=True)
            match = pattern.match(filename)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)

        print(f"Max number: {max_number}", flush=True)
        return f"ComfyUI_{max_number:05d}_.png"

    def initialize(self):
        file_name = os.path.join(__location__, "./ComfyUI/main.py")
        # self.process = subprocess.Popen(["python3.10", file_name, "--listen 0.0.0.0 --highvram"])
        # self.process = subprocess.Popen(["python3.10", file_name, "--listen 0.0.0.0 --normalvram --disable-smart-memory"])

        self.comfyUI = ComfyUI("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR, INPUT_DIR)
        
    def infer(self, inputs):
        try:
            print("Infer Started", flush=True)
            workflow = inputs["workflow"]

            print("Recieved workflow:", workflow, flush=True)

            p = {"prompt": workflow}

            data = json.dumps(p).encode("utf-8")
            print("Prompt Encoding Happened", flush=True)

            req = request.Request("http://127.0.0.1:8188/prompt", data=data)
            request.urlopen(req)

            task_completed = False
            while task_completed != True:
                response = requests.get("http://127.0.0.1:8188/queue")
                if response.json()["queue_running"] == []:
                    task_completed = True

            print("Queue Completed", flush=True)
            final_image_name = InferlessPythonModel.get_final_image_name(
                "/var/nfs-mount/Passion-ComfyUI-Volumes/output"
            )
            image_path = f"/var/nfs-mount/Passion-ComfyUI-Volumes/output/{final_image_name}"
            base64_image = InferlessPythonModel.process_single_image(image_path)

            return {"generated_image": base64_image}
        except Exception as e:
            print(f"Error processing: {e}", flush=True)
            return e
        
    def finalize(self):
        print("Finalizing", flush=True)
        # self.pipe = None
        # self.process.terminate()

        self.comfyUI.clear_queue()
        for directory in [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)


