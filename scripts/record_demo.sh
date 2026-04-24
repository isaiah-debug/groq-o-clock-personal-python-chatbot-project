#!/usr/bin/env bash
set -euo pipefail

if ! command -v vhs >/dev/null 2>&1; then
    echo "error: vhs is not installed"
    echo "install it with: brew install vhs"
    exit 1
fi

if [ -z "${GROQ_API_KEY:-}" ]; then
    echo "error: GROQ_API_KEY is not set"
    echo "export GROQ_API_KEY=your_api_key_here"
    exit 1
fi

mkdir -p itest
printf 'DocChat docs\nneedle line\n' > itest/sample.txt
vhs demo.tape
