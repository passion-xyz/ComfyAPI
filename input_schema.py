INPUT_SCHEMA = {
    "workflow_file_name": {
        'datatype': 'BYTES',
        'required': True,
        'shape': [1],
        'example': ["txt_2_img"]
    },
    "positive_token": {
        'datatype': 'BYTES',
        'required': True,
        'shape': [1],
        'example': ["There is a fine house in the forest"]
    },
    "negative_token": {
        'datatype': 'BYTES',
        'required': True,
        'shape': [1],
        'example': ["There is a fine house in the forest"]
    }
}