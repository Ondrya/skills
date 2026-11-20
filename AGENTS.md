# Instructions for agents working in this repository

This repository stores portable Agent Skills. Keep it compatible with opencode and Claude Code.

## Rules

- A skill is `skills/<id>/SKILL.md`. The directory name is the skill ID and must equal `name`.
- Never create nested skill directories such as `skills/<category>/<id>/SKILL.md`.
- Use lowercase kebab-case IDs: `^[a-z0-9]+(-[a-z0-9]+)*$`.
- Required frontmatter: `name`, `description`, `metadata.category`, `metadata.tags`,
  `metadata.version`. Add `license: MIT`.
- Allowed categories: `code`, `architecture`, `devops`, `testing`, `security`, `data`, `process`,
  `product`.
- Keep `SKILL.md` under 500 lines; put details in `references/`, helpers in `scripts/`.
- Use relative paths only. Never add secrets or machine-specific absolute paths.
- Do not edit `templates/skill/SKILL.md` when adding a skill.
- After any skill change run `make validate && make catalog`. Run `make check` before finishing.
- Do not edit `catalog.json` or the README catalog table by hand; they are generated.
- Do not commit unless the user explicitly asks.
