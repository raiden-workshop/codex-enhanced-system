#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-skills.sh --source <skills-dir> --target <codex-skills-dir> [--mode symlink|copy]

Installs each direct subdirectory containing a SKILL.md file from the source
directory into the target Codex skills directory.
EOF
}

source_dir=""
target_dir=""
mode="symlink"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      source_dir="${2:-}"
      shift 2
      ;;
    --target)
      target_dir="${2:-}"
      shift 2
      ;;
    --mode)
      mode="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$source_dir" || -z "$target_dir" ]]; then
  usage >&2
  exit 1
fi

if [[ ! -d "$source_dir" ]]; then
  echo "Source directory not found: $source_dir" >&2
  exit 1
fi

mkdir -p "$target_dir"

installed=0
while IFS= read -r -d '' skill_dir; do
  skill_name="$(basename "$skill_dir")"
  skill_target="$target_dir/$skill_name"

  case "$mode" in
    symlink)
      ln -sfn "$skill_dir" "$skill_target"
      ;;
    copy)
      rm -rf "$skill_target"
      cp -R "$skill_dir" "$skill_target"
      ;;
    *)
      echo "Unsupported mode: $mode" >&2
      exit 1
      ;;
  esac

  installed=$((installed + 1))
  printf 'Installed skill: %s\n' "$skill_name"
done < <(find "$source_dir" -mindepth 1 -maxdepth 1 -type d -name '*' -print0)

if [[ "$installed" -eq 0 ]]; then
  echo "No skills found in: $source_dir" >&2
  exit 1
fi

printf 'Skills installed into: %s\n' "$target_dir"

