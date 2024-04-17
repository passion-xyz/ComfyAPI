from io import BytesIO
import os
import base64
import subprocess

class InferlessPythonModel:
    def initialize(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        script_path = os.path.join(__location__, "custom_nodes_setup.sh")
        print(f"Running {script_path}")
        result = subprocess.run([f"ls {__location__}"], capture_output=True, text=True)
        print(result)

        result = subprocess.run([f"ls {script_path}"], capture_output=True, text=True)
        print(result)

        result = subprocess.run([f"cat {script_path}"], capture_output=True, text=True)
        print(result)

        result = subprocess.run([f"sh {script_path}"], capture_output=True, text=True)
        print(result)
        
    def infer(self, inputs):
        prompt = inputs["prompt"]
        return { "generated_image_base64" : prompt }
        
    def finalize(self):
        self.pipe = None
