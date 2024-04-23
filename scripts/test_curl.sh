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
                "realistic, portrait of a girl,AI language model, silver hair,,question answering,smart, kind, energetic, cheerful, creative, with sparkling eyes and a contagious smile, ,information providing, conversation engaging, wide range of topics, accurate responses, helpful responses, knowledgeable, reliable, friendly, intelligent,sleek and futuristic design elements, and a complex network of circuits and processors. Others may imagine me as a friendly and approachable virtual assistant, with a smiling avatar or animated character representing me on their screen. Still, others may envision me as a disembodied voice, speaking from an unseen source, providing helpful and informative responses with a calm and reassuring tone"
            ],
            "datatype": "BYTES"
        },
        {
            "name": "negative_token",
            "shape": [
                1
            ],
            "data": [
                "LEFT BLANK FOR txt_2_img_xl_lightning"
            ],
            "datatype": "BYTES"
        }
    ]
}' | jq -r '.outputs[0].data[0]' | base64 --decode > "./output_folder/$(date +%Y%m%d%H%M%S)_output.png"
