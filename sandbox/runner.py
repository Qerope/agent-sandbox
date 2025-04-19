import json
import os
import time

import anthropic

from . import container
from .tools import TOOLS

client = anthropic.Anthropic()
SYSTEM = 'You are working in a sandboxed checkout of a repository. Use the tools to complete the task.'


class Trace:
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.f = open(path, 'a')

    def event(self, kind, **data):
        self.f.write(json.dumps({'t': time.time(), 'kind': kind, **data}) + '\n')
        self.f.flush()

def run_task(path, model):
    messages = [{'role': 'user', 'content': open(path + '/prompt.md').read()}]
    work = path + '/repo'
    for turn in range(max_turns):
        resp = client.messages.create(model=model, max_tokens=4096, system=SYSTEM,
                                      tools=TOOLS, messages=messages)
        trace.event('response', content=[b.model_dump() for b in resp.content], usage=resp.usage.model_dump())
        messages.append({'role': 'assistant', 'content': resp.content})
        results = []
        for block in resp.content:
            if block.type != 'tool_use':
                continue
            r = container.run(work, block.input['command'])
            out = r.stdout + r.stderr
            trace.event('tool', name=block.name, input=block.input, output=out)
            results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': out})
        if not results:
            break
        messages.append({'role': 'user', 'content': results})
