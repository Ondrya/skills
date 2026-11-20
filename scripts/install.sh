#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
MODE="install"
COPY=0
DRY_RUN=0
TARGETS=()

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [options]

Link or copy every skill into agent discovery directories.

Options:
  --target <opencode|claude|all|path>  Target directory (repeatable).
                                       Default: opencode and claude.
  --copy                               Copy instead of symlinking.
  --uninstall                          Remove links that point into this repository.
  --dry-run                            Print actions without changing anything.
  -h, --help                           Show this help.
EOF
}

add_target() {
  case "$1" in
    opencode) TARGETS+=("$HOME/.config/opencode/skills") ;;
    claude) TARGETS+=("$HOME/.claude/skills") ;;
    all)
      TARGETS+=("$HOME/.config/opencode/skills")
      TARGETS+=("$HOME/.claude/skills")
      ;;
    *) TARGETS+=("$1") ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { echo "error: --target requires a value" >&2; exit 2; }
      add_target "$2"
      shift 2
      ;;
    --copy) COPY=1; shift ;;
    --uninstall) MODE="uninstall"; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  add_target all
fi

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "error: $SKILLS_DIR does not exist" >&2
  exit 1
fi

run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

linked=0
removed=0
already=0
skipped=0
conflicts=0

for target in "${TARGETS[@]}"; do
  if [[ "$MODE" == "install" && $DRY_RUN -eq 0 ]]; then
    mkdir -p "$target"
  fi

  for source in "$SKILLS_DIR"/*/; do
    [[ -f "${source}SKILL.md" ]] || continue
    source="${source%/}"
    id="$(basename "$source")"
    destination="$target/$id"

    if [[ "$MODE" == "uninstall" ]]; then
      if [[ -L "$destination" ]]; then
        current="$(readlink -f "$destination" 2>/dev/null || true)"
        expected="$(readlink -f "$source" 2>/dev/null || true)"
        if [[ -n "$current" && "$current" == "$expected" ]]; then
          run rm "$destination"
          removed=$((removed + 1))
        else
          printf 'skip (not managed by this repository): %s\n' "$destination" >&2
          skipped=$((skipped + 1))
        fi
      elif [[ -e "$destination" ]]; then
        printf 'skip (not a symlink): %s\n' "$destination" >&2
        skipped=$((skipped + 1))
      fi
      continue
    fi

    if [[ -L "$destination" ]]; then
      current="$(readlink -f "$destination" 2>/dev/null || true)"
      expected="$(readlink -f "$source" 2>/dev/null || true)"
      if [[ -n "$current" && "$current" == "$expected" ]]; then
        already=$((already + 1))
        continue
      fi
      printf 'conflict (symlink exists, not managed): %s\n' "$destination" >&2
      conflicts=$((conflicts + 1))
      continue
    fi

    if [[ -e "$destination" ]]; then
      printf 'conflict (path exists, back it up first): %s\n' "$destination" >&2
      conflicts=$((conflicts + 1))
      continue
    fi

    if [[ $COPY -eq 1 ]]; then
      run cp -R "$source" "$destination"
    else
      run ln -s "$source" "$destination"
    fi
    linked=$((linked + 1))
  done
done

if [[ "$MODE" == "uninstall" ]]; then
  echo "removed $removed link(s), skipped $skipped"
else
  echo "installed $linked skill(s), already linked $already, conflicts $conflicts"
fi

if [[ $conflicts -gt 0 ]]; then
  exit 1
fi
