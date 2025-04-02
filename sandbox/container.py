import subprocess


def run(workdir, cmd):
    subprocess.run(['docker', 'run', '--rm', '-v', workdir + ':/work', '-w', '/work',
                    'python:3.12-slim', 'bash', '-c', cmd])
