# agent-sandbox

Runs an LLM coding agent on a task inside a container and records what
happened.

    export ANTHROPIC_API_KEY=...
    python -m sandbox run tasks/fizzbuzz --model $AGENT_MODEL --parallel 4
    python -m sandbox replay traces/fizzbuzz-0.jsonl
    python -m sandbox report traces/
    python -m sandbox view traces/fizzbuzz-0.jsonl > view.html

A task is a directory with `prompt.md`, a `repo/` snapshot and a `check.sh`
that exits 0 when the task is solved. The agent has two tools: `bash` and
`apply_patch`. Containers have no network, a memory limit and a pids limit;
only the working directory is writable.

Traces are jsonl, one event per line: model request, tool call, tool result,
check result.
