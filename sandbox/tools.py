BASH = {
    'name': 'bash',
    'description': 'Run a shell command in the sandbox working directory.',
    'input_schema': {
        'type': 'object',
        'properties': {'command': {'type': 'string'}},
        'required': ['command'],
    },
}

APPLY_PATCH = {
    'name': 'apply_patch',
    'description': 'Apply a unified diff to the working directory.',
    'input_schema': {
        'type': 'object',
        'properties': {'diff': {'type': 'string'}},
        'required': ['diff'],
    },
}


def apply_patch(workdir, diff):
    p = subprocess.run(['patch', '-p1', '--batch'], input=diff, cwd=workdir, capture_output=True, text=True)
    return p.stdout + p.stderr, p.returncode
TOOLS = [BASH, APPLY_PATCH]
