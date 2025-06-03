import json
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
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


def load_task(path):
    work = tempfile.mkdtemp(prefix='task-')
    shutil.copytree(os.path.join(path, 'repo'), work, dirs_exist_ok=True)
    prompt = open(os.path.join(path, 'prompt.md')).read()
    return work, prompt, os.path.join(path, 'check.sh')

def run_task(path, model, max_turns=30, max_tokens=200_000, profile='docker'):
    work, prompt, check = load_task(path)
    name = os.path.basename(path.rstrip('/'))
    trace = Trace('traces/%s-%d.jsonl' % (name, int(time.time())))
    messages = [{'role': 'user', 'content': prompt}]
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

    r = subprocess.run(['bash', check], cwd=work, capture_output=True, text=True)
    trace.event('check', passed=r.returncode == 0, output=(r.stdout + r.stderr)[-2000:])
    return r.returncode == 0


def run_many(tasks, args):
    with ThreadPoolExecutor(args.parallel) as pool:
        futures = [pool.submit(run_task, t, args.model, args.max_turns) for t in tasks]
        return [f.result() for f in futures]
