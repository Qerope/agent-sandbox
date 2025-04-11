BASH = {
    'name': 'bash',
    'description': 'Run a shell command in the sandbox working directory.',
    'input_schema': {
        'type': 'object',
        'properties': {'command': {'type': 'string'}},
        'required': ['command'],
    },
}
TOOLS = [BASH]
