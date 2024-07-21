valid_schema_one_user = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "integer"},
        "first_name": {"type": "integer"},
        "last_name": {"type": "integer"},
        "avatar": {"type": "integer"},
    },
    "required": [
        "id",
        "email",
        "first_name",
        "last_name",
        "avatar"
    ]
}

valid_schema_all_users = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "email": {"type": "integer"},
            "first_name": {"type": "integer"},
            "last_name": {"type": "integer"},
            "avatar": {"type": "integer"},
        },
    },
}
