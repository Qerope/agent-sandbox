import glob
import json

from rich.console import Console
from rich.table import Table


def report(dirname):
    t = Table('trace', 'turns', 'tokens', 'result')
    for path in sorted(glob.glob(dirname + '/*.jsonl')):
        turns = tokens = 0
        result = '?'
        for line in open(path):
            e = json.loads(line)
            if e['kind'] == 'response':
                turns += 1
                tokens += e['usage']['input_tokens'] + e['usage']['output_tokens']
            elif e['kind'] == 'check':
                result = 'pass' if e['passed'] else 'fail'
        t.add_row(path.split('/')[-1], str(turns), str(tokens), result)
    Console().print(t)
