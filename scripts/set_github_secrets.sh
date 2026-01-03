#!/usr/bin/env bash
SECRETS_FILE=${1:-secrets.json}
if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install from https://cli.github.com/."
  exit 1
fi
if [ ! -f "$SECRETS_FILE" ]; then
  echo "Secrets file not found: $SECRETS_FILE"
  exit 1
fi
while IFS="=" read -r key value; do
  if [ -z "$key" ]; then
    continue
  fi
  echo "Setting secret: $key"
  gh secret set "$key" --body "$value"
done < <(jq -r 'to_entries|map("\(.key)=\(.value)")|.[]' "$SECRETS_FILE")
