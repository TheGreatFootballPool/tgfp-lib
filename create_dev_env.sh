#!/usr/bin/env bash
set -o allexport
ENVIRONMENT=development
# Building the stack environment file
op inject -f -i op.env -o stack.env
source stack.env
