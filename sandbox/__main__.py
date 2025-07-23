import argparse
import os

from . import runner
from . import replay


def main():
    ap = argparse.ArgumentParser(prog='sandbox')
    sub = ap.add_subparsers(dest='cmd', required=True)
    run = sub.add_parser('run')
    run.add_argument('task')
    run.add_argument('--model', default=os.environ.get('AGENT_MODEL'), required='AGENT_MODEL' not in os.environ)
    run.add_argument('--max-turns', type=int, default=30)
    run.add_argument('--parallel', type=int, default=1)
    rp = sub.add_parser('replay')
    rp.add_argument('trace')
    args = ap.parse_args()
    if args.cmd == 'run':
        runner.run_many([args.task], args)
    elif args.cmd == 'replay':
        replay.replay(args.trace)


if __name__ == '__main__':
    main()
