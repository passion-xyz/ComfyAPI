from io import BytesIO
import base64
import subprocess

class InferlessPythonModel:
    def initialize(self):
        result = subprocess.run(['bash ./custom_nodes_setup.sh'], capture_output=True, text=True)
        
    def infer(self, inputs):
        prompt = inputs["prompt"]
        return { "generated_image_base64" : prompt }
        
    def finalize(self):
        self.pipe = None
