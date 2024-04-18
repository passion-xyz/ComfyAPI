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
            return None
        
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
        import subprocess

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        file_name = os.path.join(__location__, "main.py")
        self.process = subprocess.Popen(["python3.10", file_name])
        
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
            return None
        
    def finalize(self):
        self.pipe = None
        self.process.terminate()
        print("Finalizing", flush=True)

