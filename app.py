from io import BytesIO
import os
import base64
import sys
import subprocess

class InferlessPythonModel:
    def initialize(self):
        import subprocess

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        file_name = os.path.join(__location__, "main.py")
        self.process = subprocess.Popen(["python3.10", file_name])
        mounted_path = '/var/nfs-mount/Passion-ComfyUI-Volumes'
        sys.path.insert(1, mounted_path)
        try:
            ls_output = subprocess.check_output(['ls', mounted_path])
            print("Contents of the mounted path:", ls_output.decode())
        except subprocess.CalledProcessError as e:
            print("Failed to list contents of the mounted path:", e)
        
    def infer(self, inputs):
        print(inputs)
        # prompt = inputs["prompt"]
        return { "generated_image_base64" : 'prompt' }
        
    def finalize(self):
        self.pipe = None
        self.process.terminate()
        print("Finalizing", flush=True)

