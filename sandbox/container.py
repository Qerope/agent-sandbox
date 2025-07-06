import subprocess
from dataclasses import dataclass
import uuid

@dataclass
class Result:
    stdout: str
    stderr: str
    code: int
    timed_out: bool = False


def tail(s, n=8000):
    return s if len(s) <= n else '... [truncated] ...\n' + s[-n:]


def run(workdir, cmd, timeout=60):
    name = 'sandbox-' + uuid.uuid4().hex[:8]
    args = ['docker', 'run', '--rm', '--name', name]
    args += ['--network', 'none']
    args += ['-v', workdir + ':/work', '-w', '/work', 'python:3.12-slim', 'bash', '-c', cmd]
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        subprocess.run(['docker', 'kill', name], capture_output=True)
        return Result('', 'timed out after %ds' % timeout, 124, True)
    except BaseException:
        subprocess.run(['docker', 'kill', name], capture_output=True)
        raise
    return Result(tail(p.stdout), tail(p.stderr), p.returncode)
