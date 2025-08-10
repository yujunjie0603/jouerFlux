"Configuration for Swagger API documentation"
template_swagger = {
        "swagger": "2.0",
        "info": {
            "title": "JouerFlux API",
            "version": "1.0.0",
            "description": "Firewall management endpoints"
        },
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "definitions": {
            "Firewall": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"}
                }
            },
            "FirewallWithPolicies": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"},
                    "policies": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id":   {"type": "integer"},
                                "name": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "Policy": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "name": {"type": "string"},
                }
            },
            "Rule": {
                "type": "object",
                "properties": {
                    "id":   {"type": "integer"},
                    "action": {"type": "string"},
                    "source_ip": {"type": "string"},
                    "destination_ip": {"type": "string"},
                    "protocol": {"type": "string"},
                    "port": {"type": "integer"}
                }
            }
        }
    }
