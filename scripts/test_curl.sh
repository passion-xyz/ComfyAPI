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
                "txt_2_img_RealVisXL"
            ],
            "datatype": "BYTES"
        },
        {
            "name": "positive_token",
            "shape": [
                1
            ],
            "data": [
                "Busty Vintage Spaceage by Ed Mell and Russ Mills,  (luminar , vivacious , masterful:1.4), poster art, bold lines, hyper detailed, expressive,  award winning,  (scenery:1.4), (intricate details, masterpiece, best quality:1.4),ring light , looking at viewer, dynamic pose, wide angle view, atmospheric haze, Film grain, cinematic film still, highly detailed, high budget, cinemascope, moody, epic, OverallDetail, gorgeous, 2000s vintage RAW photo, photorealistic, candid camera, color graded cinematic, eye catchlights, atmospheric lighting, skin pores, imperfections, natural, shallow dof,"
            ],
            "datatype": "BYTES"
        },
        {
            "name": "negative_token",
            "shape": [
                1
            ],
            "data": [
                "nsfw,yallow,(((pubic))), ((((pubic_hair)))),sketch, duplicate, ugly, huge eyes, text, logo, monochrome, worst face, (bad and mutated hands:1.3), (worst quality:1.7), (low quality:1.7), (blurry:1.7),horror, geometry, bad_prompt, (bad hands), (missing fingers), multiple limbs, bad anatomy, (interlocked fingers:1.2),(interlocked leg:1.2), Ugly Fingers, (extra digit and hands and fingers and legs and arms:1.4), crown braid,, (deformed fingers:1.2), (long fingers:1.2),succubus wings,horn,succubus horn,succubus hairstyle, (bad-artist-anime), bad-artist, bad hand"
            ],
            "datatype": "BYTES"
        }
    ]
}' | jq -r '.outputs[0].data[0]' | base64 --decode > "./output_folder/$(date +%Y%m%d%H%M%S)_output.png"
