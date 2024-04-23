curl --location 'https://m-66f63a8dcc79442fb2c772e3193fedd8-m.default.model-v2.inferless.com/v2/models/ComfyAPI_Dev_66f63a8dcc79442fb2c772e3193fedd8/versions/1/infer' \
          --header 'Content-Type: application/json' \
          --header 'Authorization: Bearer daa5116d2d8224e592b1db3fc3853391a3d5d91f99cb6119edaa200749c546cafba69998600fcf699057ca407e7467aa88eed323706afc0b4a9aa0e6fd765354' \
          --data '{
    "inputs": [
        {
            "name": "workflow",
            "shape": [
                1
            ],
            "data": [
                "txt_2_img_full_XL_way_upscale"
            ],
            "datatype": "BYTES"
        },
        {
            "name": "positive_token",
            "shape": [
                1
            ],
            "data": [
                "autumn best quality, ink painting, acrylic, cute ice cornflowers, sunrise, by Craola, Dan Mumford, Andy Kehoe, 2d, flat, adorable, vintage, art on a cracked paper, fairytale, storybook detailed illustration, cinematic, ultra highly detailed, tiny details, beautiful details, mystical, luminism, vibrant colors, complex background, centered, symmetry, painted, intricate, volumetric lighting, beautiful, rich deep colors masterpiece, sharp focus, ultra detailed, in the style of dan mumford and marc simonetti, astrophotography, centered, symmetry, painted, intricate, volumetric lighting, beautiful, rich deep colors masterpiece, sharp focus, ultra detailed, in the style of dan mumford and marc simonetti, astrophotography<lora:xl_more_art-full_v1:0.5>"
            ],
            "datatype": "BYTES"
        },
        {
            "name": "negative_token",
            "shape": [
                1
            ],
            "data": [
                "(worst quality, low quality:2), NSFW,monochrome, zombie,overexposure, watermark,text,bad anatomy,bad hand,((extra hands)),extra fingers,too many fingers,fused fingers,bad arm,distorted arm,extra arms,fused arms,extra legs,missing leg,disembodied leg,extra nipples, detached arm, liquid hand,inverted hand,disembodied limb, oversized head,extra body,extra navel,easynegative,(hair between eyes),sketch, duplicate, ugly, huge eyes, text, logo, worst face, (bad and mutated hands:1.3),  (blurry:2.0), horror, geometry, bad_prompt, (bad hands), (missing fingers), multiple limbs, bad anatomy, (interlocked fingers:1.2), Ugly Fingers, (extra digit and hands and fingers and legs and arms:1.4), (deformed fingers:1.2), (long fingers:1.2),(bad-artist-anime), bad-artist, bad hand, extra legs ,(ng_deepnegative_v1_75t),((hands on head))"
            ],
            "datatype": "BYTES"
        }
    ]
}' | jq -r '.outputs[0].data[0]' | base64 --decode > "./output_folder/$(date +%Y%m%d%H%M%S)_output.png"

