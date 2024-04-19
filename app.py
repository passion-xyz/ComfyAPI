import json
from urllib import request, parse
import requests
from tqdm import tqdm
import os
import asyncio
import base64
from PIL import Image
from io import BytesIO
import re
import subprocess

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

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
        file_name = os.path.join(__location__, "main.py")
        print(f"Initializing {file_name}", flush=True)
        self.process = subprocess.Popen(["python3.10", file_name,'--port','8188', '--listen','127.0.0.1'])
        print(f"Initialization Complete - Server Running {self.process}", flush=True)

    def infer(self, inputs):
        try:
            print("Infer Started", flush=True)
            workflow = inputs["workflow"]
            positive_token = inputs["positive_token"]
            negative_token = inputs["negative_token"]
            workflow_file_name = f"{workflow}.json"

            prompt = json.loads(
                open(f"{__location__}/workflows/{workflow_file_name}").read()
                .replace("$$POSITIVE_TOKEN$$", positive_token)
                .replace("$$NEGATIVE_TOKEN$$", negative_token)
            )
            
            p = {"prompt": prompt}

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

    def finalize(self, args):
        print("Finalizing", flush=True)
        self.process.terminate()


# if __name__ == "__main__":
#     model = InferlessPythonModel()
#     model.initialize()
#     ab = model.infer({"workflow": "txt_2_img", "parameters": {"prompt": "masterpiece image of a smart dog wearing a coat and tie and glasses"}})
#     model.finalize()
