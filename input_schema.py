INPUT_SCHEMA = {
    "workflow": {
        'datatype': 'BYTES',
        'required': True,
        'shape': [1],
        'example': ["SKIP"]
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