# Contributing

## Add or change a skill

1. Create `skills/<id>/SKILL.md` from `templates/skill/SKILL.md`. The directory must be the skill ID.
2. Follow the naming and frontmatter rules below.
3. Run `make validate`.
4. Run `make catalog` to update `catalog.json` and the README table.
5. Open a pull request with one logical skill change per PR.

## Naming

- ID: `^[a-z0-9]+(-[a-z0-9]+)*$`, 1-64 characters, unique.
- `name` in frontmatter must equal the directory name.
- Prefer a domain prefix when the name would otherwise be generic: `arch-api-design`,
  `dotnet-webapi`, `ops-incident-response`.

## Frontmatter

```yaml
---
name: arch-api-design
description: "Designs REST and gRPC APIs... USE FOR: ... DO NOT USE FOR: ..."
license: MIT
metadata:
  category: architecture
  tags: "api, rest, grpc, design"
  version: "0.1.0"
---
```

| Field | Required | Rules |
|---|---|---|
| `name` | yes | Must match the directory name |
| `description` | yes | 1-1024 characters. What it does and when to use it |
| `license` | no | Use `MIT` for this repository |
| `metadata.category` | yes | One of `code`, `architecture`, `devops`, `testing`, `security`, `data`, `process`, `product` |
| `metadata.tags` | yes | Comma-separated lowercase tags |
| `metadata.version` | yes | Semver string; bump when the skill behavior changes |

Write the description in the third person and include both trigger and non-trigger cases:

- `USE FOR:` tasks and keywords that should activate the skill.
- `DO NOT USE FOR:` nearby tasks that belong to another skill.

## Content

- Keep `SKILL.md` under 500 lines. Move long material to `references/` and link it with a relative
  path (`references/ref.md`).
- Keep file references one level deep from `SKILL.md`.
- Put executable helpers in `scripts/`. They must be self-contained, support `--help`, and fail with
  a clear message.
- Use relative paths only. No absolute paths, no secrets, no credentials.
- Document environment requirements in `compatibility` if the skill needs specific tools or network
  access.

## Review checklist

- [ ] `make check` passes.
- [ ] Name and directory match.
- [ ] Description explains what the skill does and when to use it.
- [ ] No secrets, credentials, or machine-specific paths.
- [ ] Supporting scripts are safe to run and documented.
