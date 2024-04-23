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
                "txt_2_img_xl_lightning"
            ],
            "datatype": "BYTES"
        },
        {
            "name": "positive_token",
            "shape": [
                1
            ],
            "data": [
                "woman, goat, hugging, affection, snow, winter, outdoor, candid, warm clothing, hat, scarf, smiling, animal bond, close-up, genuine emotion, cold weather, friendship, woolen scarf, black coat, backpack, visible breath, light snowfall, bokeh background, human-animal relationship, day time, Fujifilm XT3, Canon R5, Fujicolor Fujichrome Velvia 100"
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
}' | jq -r '.outputs[0].data[0]' | base64 --decode > output.png