VERIFICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "needs_correction": {
            "type": "boolean",
            "description": "True if the last response needs to be removed and regenerated"
        },
        "feedback": {
            "type": "string",
            "description": "Detailed explanation of what was wrong and what to fix"
        }
    },
    "required": ["needs_correction", "feedback"]
}
