#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
skills_home="$codex_home/skills"

if [[ ! -d "$repo_root/.git" ]]; then
  echo "This script must be run from a checkout of codex-enhanced-system." >&2
  exit 1
fi

mkdir -p "$codex_home"
mkdir -p "$skills_home"

echo "Installing method-forge skills into: $skills_home"
"$script_dir/install-skills.sh" \
  --source "$repo_root/method-forge/skills" \
  --target "$skills_home" \
  --mode symlink

cat <<EOF
Done.

Next steps:
1. Open this repository as a Codex workspace.
2. Keep the clone updated with git pull.
3. Re-run this bootstrap script after skill changes.

Repo: $repo_root
Codex home: $codex_home
EOF

