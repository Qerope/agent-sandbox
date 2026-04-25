import argparse
import os

from . import runner
from . import replay
from . import report
from . import view


def main():
    ap = argparse.ArgumentParser(prog='sandbox')
    sub = ap.add_subparsers(dest='cmd', required=True)
    run = sub.add_parser('run')
    run.add_argument('task')
    run.add_argument('--model', default=os.environ.get('AGENT_MODEL'), required='AGENT_MODEL' not in os.environ)
    run.add_argument('--max-turns', type=int, default=30)
    run.add_argument('--parallel', type=int, default=1)
    run.add_argument('--max-tokens', type=int, default=200_000)
    rp = sub.add_parser('replay')
    rp.add_argument('trace')
    rep = sub.add_parser('report')
    rep.add_argument('dir')
    vw = sub.add_parser('view')
    vw.add_argument('trace')
    args = ap.parse_args()
    if args.cmd == 'run':
        runner.run_many([args.task], args)
    elif args.cmd == 'replay':
        replay.replay(args.trace)
    elif args.cmd == 'report':
        report.report(args.dir)
    elif args.cmd == 'view':
        print(view.render(args.trace))


if __name__ == '__main__':
    main()
