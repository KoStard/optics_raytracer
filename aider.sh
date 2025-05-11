#!/bin/bash

# Editable file
# editable_file="./docs/tasks.md"

# Files to mark as read-only (philosophy.md and all __init__.py files)
read_only_files=("./docs/philosophy.md")
while IFS= read -r file; do
  read_only_files+=("$file")
done < <(find src -type f -name "*.py")

# Build the aider command
cmd="aider"
for file in "${read_only_files[@]}"; do
  cmd+=" --read \"$file\""
done
# cmd+=" --file \"$editable_file\""

# Execute the command
eval "$cmd"