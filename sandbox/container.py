import subprocess
from dataclasses import dataclass

@dataclass
class Result:
    stdout: str
    stderr: str
    code: int

def run(workdir, cmd):
    p = subprocess.run(['docker', 'run', '--rm', '-v', workdir + ':/work', '-w', '/work',
                        'python:3.12-slim', 'bash', '-c', cmd], capture_output=True, text=True)
    return Result(p.stdout, p.stderr, p.returncode)
