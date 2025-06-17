schema_get_owners = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "address": {"type": "string"},
            "city": {"type": "string"},
            "telephone": {"type": "string"},
            "id": {"type": "integer"},
            "pets": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "birthDate": {"type": "string", "format": "date"},
                        "type": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "id": {"type": "integer"}
                            },
                            "required": ["name", "id"],
                            "additionalProperties": False
                        },
                        "id": {"type": "integer"},
                        "ownerId": {"type": "integer"},
                        "visits": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "date": {"type": "string", "format": "date"},
                                    "description": {"type": "string"},
                                    "id": {"type": "integer"},
                                    "petId": {"type": "integer"}
                                },
                                "required": ["date", "description", "id", "petId"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["name", "birthDate", "type", "id", "ownerId", "visits"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["firstName", "lastName", "address", "city", "telephone", "id", "pets"],
        "additionalProperties": False
    }
}