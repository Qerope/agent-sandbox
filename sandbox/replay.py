import json


def replay(path):
    for line in open(path):
        e = json.loads(line)
        if e['kind'] == 'tool':
            print('$', e['input'].get('command') or e['input'].get('diff', '')[:200])
            print(e['output'])
        elif e['kind'] == 'check':
            print('CHECK', 'pass' if e['passed'] else 'fail')
