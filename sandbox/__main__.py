import argparse
import os

from . import runner


def main():
    ap = argparse.ArgumentParser(prog='sandbox')
    sub = ap.add_subparsers(dest='cmd', required=True)
    run = sub.add_parser('run')
    run.add_argument('task')
    run.add_argument('--model', default=os.environ.get('AGENT_MODEL'), required='AGENT_MODEL' not in os.environ)
    args = ap.parse_args()
    runner.run_task(args.task, args.model)


if __name__ == '__main__':
    main()
