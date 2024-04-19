import subprocess
import time
import os
import json

from helpers.ComfyUI_Controlnet_Aux import ComfyUI_Controlnet_Aux
from helpers.ComfyUI_AnimateDiff_Evolved import ComfyUI_AnimateDiff_Evolved
from helpers.ComfyUI_BRIA_AI_RMBG import ComfyUI_BRIA_AI_RMBG
from helpers.WAS_Node_Suite import WAS_Node_Suite

UPDATED_WEIGHTS_MANIFEST_URL = f"https://weights.replicate.delivery/default/comfy-ui/weights.json?cache_bypass={int(time.time())}"
UPDATED_WEIGHTS_MANIFEST_PATH = "updated_weights.json"
WEIGHTS_MANIFEST_PATH = "weights.json"

BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
BASE_PATH = "ComfyUI/models"


class WeightsManifest:
    def __init__(self):
        self.weights_manifest = self._load_weights_manifest()
        self.weights_map = self._initialize_weights_map()

    def _load_weights_manifest(self):
        self._download_updated_weights_manifest()
        return self._merge_manifests()

    def _download_updated_weights_manifest(self):
        if not os.path.exists(UPDATED_WEIGHTS_MANIFEST_PATH):
            print(
                f"Downloading updated weights manifest from {UPDATED_WEIGHTS_MANIFEST_URL}"
            )
            start = time.time()
            subprocess.check_call(
                [
                    "pget",
                    "--log-level",
                    "warn",
                    "-f",
                    UPDATED_WEIGHTS_MANIFEST_URL,
                    UPDATED_WEIGHTS_MANIFEST_PATH,
                ],
                close_fds=False,
            )
            print(
                f"Downloading {UPDATED_WEIGHTS_MANIFEST_URL} took: {(time.time() - start):.2f}s"
            )
        else:
            print("Updated weights manifest file already exists")

    def _merge_manifests(self):
        if os.path.exists(WEIGHTS_MANIFEST_PATH):
            with open(WEIGHTS_MANIFEST_PATH, "r") as f:
                original_manifest = json.load(f)
        else:
            original_manifest = {}

        with open(UPDATED_WEIGHTS_MANIFEST_PATH, "r") as f:
            updated_manifest = json.load(f)

        for key in updated_manifest:
            if key in original_manifest:
                for item in updated_manifest[key]:
                    if item not in original_manifest[key]:
                        print(f"Adding {item} to {key}")
                        original_manifest[key].append(item)
            else:
                original_manifest[key] = updated_manifest[key]

        return original_manifest

    def _generate_weights_map(self, keys, dest):
        custom_weights = {
            # "zavychromaxl_v31.safetensors": "https://weights.replicate.delivery/default/basedlabs-media/zavychromaxl_v31.safetensors.tar",
            # "nightvisionXLPhotorealisticPortrait_v0791Bakedvae.safetensors": "https://storage.googleapis.com/basedlabs-media/nightvisionXLPhotorealisticPortrait_v0791Bakedvae.safetensors.tar",
            # "kitty.safetensors": "https://weights.replicate.delivery/default/basedlabs-media/kitty.safetensors.tar",
            # "rife47.pth": "https://weights.replicate.delivery/default/basedlabs-media/rife47.pth.tar",
            # "svd_xt_1_1.safetensors": "https://weights.replicate.delivery/default/basedlabs-media/svd_xt_1_1.safetensors.tar",
            # "XL_VAE_C1.safetensors": "https://storage.googleapis.com/basedlabs-media/XL_VAE_C1.safetensors.tar",
            # "pixelArtDiffusionXL_pixelWorld.safetensors": "https://storage.googleapis.com/basedlabs-media/pixelArtDiffusionXL_pixelWorld.safetensors.tar",
            # "ral-dissolve-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-dissolve-sdxl.safetensors.tar",
            # "ral-frctlgmtry-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-frctlgmtry-sdxl.safetensors.tar",
            # "ral-elctryzt-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-elctryzt-sdxl.safetensors.tar",
            # "EldritchComicsXL1.2.safetensors": "https://storage.googleapis.com/basedlabs-media/EldritchComicsXL1.2.safetensors.tar",
            # "ral-vlntxplzn-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-vlntxplzn-sdxl.safetensors.tar",
            # "ral-bling-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-bling-sdxl.safetensors.tar",

            # "ral-glydch-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-glydch-sdxl.safetensors.tar",
            # "ral-polygon-sdxl.safetensors": "https://storage.googleapis.com/basedlabs-media/ral-polygon-sdxl.safetensors.tar",
            # "Particles_Style_SDXL.safetensors": "https://storage.googleapis.com/basedlabs-media/Particles_Style_SDXL.safetensors.tar",

            "NijiExpressive_V2_v1.0.safetensors": "https://ai-models.passion.xyz/NijiExpressive_V2_v1.0.safetensors.tar",
            "mercury_v2.safetensors": "https://ai-models.passion.xyz/mercury_v2.safetensors.tar",
            "juggernautXL_v9Rdphoto2Lightning.safetensors": "https://ai-models.passion.xyz/juggernautXL_v9Rdphoto2Lightning.safetensors.tar",
            "AWPainting_v1.3.safetensors": "https://ai-models.passion.xyz/AWPainting_v1.3.safetensors.tar",
            "anything_inkBase.safetensors": "https://ai-models.passion.xyz/anything_inkBase.safetensors.tar",
            "animagineXLV3_v30.safetensors": "https://ai-models.passion.xyz/animagineXLV3_v30.safetensors.tar",
        }

        return {
            key: {
                "url": custom_weights[key] if key in custom_weights else f"{BASE_URL}/{dest}/{key}.tar",
                "dest": f"{BASE_PATH}/{dest}"
            }
            for key in keys
        }

    def _initialize_weights_map(self):
        weights_map = {}
        for key in self.weights_manifest.keys():
            if key.isupper():
                weights_map.update(
                    self._generate_weights_map(self.weights_manifest[key], key.lower())
                )
        weights_map.update(ComfyUI_Controlnet_Aux.weights_map(BASE_URL))
        weights_map.update(ComfyUI_AnimateDiff_Evolved.weights_map(BASE_URL))
        weights_map.update(WAS_Node_Suite.weights_map(BASE_URL))
        weights_map.update(ComfyUI_BRIA_AI_RMBG.weights_map(BASE_URL))

        print("Allowed weights:")
        for weight in weights_map.keys():
            print(weight)

        return weights_map

    def non_commercial_weights(self):
        return [
            "inswapper_128.onnx",
            "inswapper_128_fp16.onnx",
            "proteus_v02.safetensors",
            "RealVisXL_V3.0_Turbo.safetensors",
            "sd_xl_turbo_1.0.safetensors",
            "sd_xl_turbo_1.0_fp16.safetensors",
            "svd.safetensors",
            "svd_xt.safetensors",
            "turbovisionxlSuperFastXLBasedOnNew_tvxlV32Bakedvae",
            "copaxTimelessxlSDXL1_v8.safetensors",
            "MODILL_XL_0.27_RC.safetensors",
            "epicrealismXL_v10.safetensors",
        ]

    def is_non_commercial_only(self, weight_str):
        return weight_str in self.non_commercial_weights()

    def get_weights_by_type(self, weight_type):
        return self.weights_manifest.get(weight_type, [])

    def write_supported_weights(self):
        weight_lists = {
            "Checkpoints": self.get_weights_by_type("CHECKPOINTS"),
            "Upscale models": self.get_weights_by_type("UPSCALE_MODELS"),
            "CLIP Vision": self.get_weights_by_type("CLIP_VISION"),
            "LORAs": self.get_weights_by_type("LORAS"),
            "Embeddings": self.get_weights_by_type("EMBEDDINGS"),
            "IPAdapter": self.get_weights_by_type("IPADAPTER"),
            "ControlNet": self.get_weights_by_type("CONTROLNET"),
            "VAE": self.get_weights_by_type("VAE"),
            "UNets": self.get_weights_by_type("UNET"),
            "PhotoMaker": self.get_weights_by_type("PHOTOMAKER"),
            "InstantID": self.get_weights_by_type("INSTANTID"),
            "InsightFace": self.get_weights_by_type("INSIGHTFACE"),
            "Ultralytics": self.get_weights_by_type("ULTRALYTICS"),
            "Segment anything models (SAM)": self.get_weights_by_type("SAMS"),
            "GroundingDino": self.get_weights_by_type("GROUNDING-DINO"),
            "MMDets": self.get_weights_by_type("MMDETS"),
            "Face restoration models": self.get_weights_by_type("FACERESTORE_MODELS"),
            "Face detection models": self.get_weights_by_type("FACEDETECTION"),
            "AnimateDiff": ComfyUI_AnimateDiff_Evolved.models(),
            "AnimateDiff LORAs": ComfyUI_AnimateDiff_Evolved.loras(),
            "ControlNet Preprocessors": sorted(
                {
                    f"{repo}/{filename}"
                    for filename, repo in ComfyUI_Controlnet_Aux.models().items()
                }
            ),
        }
        with open("supported_weights.md", "w") as f:
            for weight_type, weights in weight_lists.items():
                f.write(f"## {weight_type}\n\n")
                for weight in weights:
                    f.write(f"- {weight}\n")
                f.write("\n")