# API Evolution and Stability

Use this reference during Step 6. Write every decision into the project's own document; do not leave
compatibility policy implicit.

## Mandatory decisions before launch

1. What counts as a **breaking change** for this API and these consumers?
2. How are **new fields** introduced? Optional additions are normally non-breaking.
3. How are **new operations** introduced? Additions are normally non-breaking.
4. Which **versioning strategy** is used: URL path, header, or media type? Why?
5. What is the **deprecation process**: notice period, communication channel, sunset date?

## Compatibility examples

| Change | Classification | Notes |
| --- | --- | --- |
| Add an optional response field | Non-breaking | Consumers must tolerate unknown fields |
| Add a new endpoint | Non-breaking | Document and lint it |
| Add an optional request field | Usually non-breaking | Define behavior when it is absent |
| Add a required request field | Breaking | Existing callers cannot satisfy it |
| Remove or rename a field | Breaking | Requires a new major version or migration |
| Change a field type or format | Breaking | Even if most values still parse |
| Tighten validation or enum values | Breaking | Previously accepted input now fails |
| Change a status code for the same outcome | Breaking | Clients branch on status codes |
| Change default pagination or limits | Potentially breaking | Depends on consumer assumptions |

Treat this table as a starting point. The project-specific definition wins, and it must be recorded.

## Template: versioning decision

```markdown
### Versioning decision

- **Approach:** URL path | header | media type
- **Rationale:** <consumer constraints, caching, gateway support, operational cost>
- **How a new version is introduced:** <process and approval>
- **Support policy for old versions:** <duration and conditions>
- **Communication plan:** <changelog, notices, deprecation headers>
```

## Template: non-breaking extension

```markdown
### Non-breaking extension

- **What is added:** <field or operation>
- **Why it is non-breaking:** <consumer behavior and tolerance>
- **Default or absent-value behavior:** <semantics>
- **How consumers learn about it:** <changelog, docs, release note>
```

## Template: breaking change

```markdown
### Breaking change

- **What changes:** <contract fragment>
- **Why it cannot be avoided:** <evidence>
- **Migration path for consumers:** <steps and tooling>
- **Deprecation plan:** <notice period, communication, sunset date>
- **Rollback plan:** <what happens if migration stalls>
```

## Deprecation checklist

- [ ] The replacement is available and documented before the old behavior is deprecated.
- [ ] The deprecation is visible in the contract and, where supported, in response headers.
- [ ] Every known consumer has an owner and a migration contact.
- [ ] The sunset date is realistic and communicated more than once.
- [ ] Monitoring shows whether traffic still depends on the deprecated behavior.
- [ ] Removal happens only after the sunset date and a final usage check.
