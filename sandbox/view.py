import html
import json


def render(path):
    rows = []
    for line in open(path):
        e = json.loads(line)
        if e['kind'] == 'tool':
            cmd = e['input'].get('command') or e['input'].get('diff', '')
            rows.append('<pre class="cmd">$ %s</pre><pre>%s</pre>' % (html.escape(cmd), html.escape(e['output'])))
        elif e['kind'] == 'check':
            rows.append('<h3>check: %s</h3>' % ('pass' if e['passed'] else 'fail'))
    return '<!doctype html><meta charset="utf-8"><style>pre{background:#f4f4f4;padding:6px}.cmd{background:#e8eefc}</style>' + ''.join(rows)
