valid_schema_one_user = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "avatar": {"type": "string"},
    },
    "required": [
        "id",
        "first_name",
        "last_name",
        "email",
        "avatar"
    ]
}


valid_schema_all_users = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "email": {"type": "string"},
            "avatar": {"type": "string"},
        },
        "required": ["id", "first_name", "last_name", "email", "avatar"]
    }
}
