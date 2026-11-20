# API Design and Audit Checklist

Use this flat checklist for reviews, then group findings by category for the report. Each item cites
the chapter of *The Design of Web APIs, 2nd edition* that motivates it.

Verdicts: `pass`, `fail`, `n/a`. A `fail` needs evidence: the operation, file, or contract fragment.
A category is complete only when every item has a verdict.

## Category A. Requirements and capabilities (Chapter 2)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| A1 | The API reflects consumer needs, not the internal database structure | ☐ | 2 |
| A2 | The capability list is fixed and agreed with the business | ☐ | 2 |
| A3 | Every capability has a named target consumer | ☐ | 2 |

## Category B. Data (Chapters 5, 8)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| B1 | Field names are consistent across the API | ☐ | 8 |
| B2 | The error format is identical for all operations | ☐ | 8 |
| B3 | Optional and nullable fields are handled predictably | ☐ | 8 |
| B4 | The data model is not a copy of the database schema | ☐ | 5 |
| B5 | Data schemas are documented in JSON Schema | ☐ | 7 |

## Category C. Operations (Chapters 4, 9)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| C1 | HTTP methods follow semantics: GET is safe, PUT is idempotent | ☐ | 4 |
| C2 | Status codes are correct: 200, 201, 204, 400, 404, 409, 500 | ☐ | 4 |
| C3 | Operation names are understandable without extra documentation | ☐ | 9 |
| C4 | Pagination is implemented consistently | ☐ | 9 |
| C5 | Batch and bulk operations define partial-success behavior | ☐ | 10 |

## Category D. Flows and consistency (Chapters 10-11)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| D1 | End-to-end flows (create, read, update) are covered | ☐ | 10 |
| D2 | The same concept has the same name in every endpoint | ☐ | 11 |
| D3 | Content negotiation (Accept/Content-Type) is handled | ☐ | 11 |

## Category E. Constraints (Chapters 12-14)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| E1 | Authentication is defined for every operation | ☐ | 12 |
| E2 | Authorization scopes and roles match data sensitivity | ☐ | 12 |
| E3 | Caching and field selection are available where needed | ☐ | 13 |
| E4 | Context-specific limits are accounted for: network, regulation | ☐ | 14 |

## Category F. Evolution and stability (Chapter 15)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| F1 | The definition of a breaking change is written down | ☐ | 15 |
| F2 | A versioning strategy is chosen and documented | ☐ | 15 |
| F3 | New fields are introduced as optional, non-breaking additions | ☐ | 15 |
| F4 | The deprecation process is defined and communicated | ☐ | 15 |

## Category G. Documentation and automation (Chapters 6, 16-18)

| # | Item | Verdict | Chapter |
| --- | --- | --- | --- |
| G1 | The OpenAPI document is valid and current | ☐ | 6 |
| G2 | Design guidelines are stated with rationale | ☐ | 16 |
| G3 | Spectral or equivalent rules run in CI | ☐ | 18 |

## Grouped report format

```markdown
## Summary
- Pass: <n>
- Fail: <n>
- Not applicable: <n>

## Findings by category
### A. Requirements and capabilities
- A1: fail - <evidence and consumer impact>
- A2: pass
...

## Prioritized remediation
1. <highest consumer or compatibility risk>
2. ...
```
