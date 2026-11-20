---
name: api-design-laure
description: "Designs, reviews, and audits web APIs with Arnaud Lauret's consumer-first methodology from The Design of Web APIs, 2nd edition (2025). USE FOR: turning requirements into API capabilities, modeling operations and data, HTTP/OpenAPI contracts, developer experience, security and efficiency constraints, versioning and breaking-change policy, design guidelines, Spectral linting. DO NOT USE FOR: ASP.NET Core implementation details (use dotnet-webapi), C# refactoring, gRPC/protobuf generation, or infrastructure work."
license: MIT
metadata:
  category: architecture
  tags: "api-design, rest, openapi, arnaud-laure, versioning, spectral, architecture"
  version: "0.1.0"
---

# API Design with Arnaud Lauret's Methodology

Design web APIs for consumers, not for the database. Work from business capabilities to a stable
contract, and make every decision explicit enough to survive multiple years and many teams.

This skill follows the structure of *The Design of Web APIs, Second Edition* (Arnaud Lauret, Manning,
2025). Chapter references are based on the official table of contents. Do not claim to quote the book;
use the methodology and the artifacts in `references/`.

## Operating principles

- **Consumer-first.** Name, shape, and sequence everything for the people and systems calling the API.
- **Capabilities before endpoints.** Do not start with HTTP methods, URLs, or a database schema.
- **Contract before code.** The OpenAPI document and JSON Schema are the design; implementation follows.
- **Stability is designed.** Treat compatibility, versioning, and deprecation as first-class requirements.
- **Automate quality.** Encode guidelines as lint rules, not as tribal knowledge.
- **Ask before assuming.** If the project context is missing, collect it first.

## Inputs to establish

Ask for these before producing a design or an audit:

| Input | Why it matters |
| --- | --- |
| API type: internal, partner, public, or mixed | Sets documentation, compatibility, and review rigor |
| Expected lifetime | Drives versioning and deprecation policy |
| Consumers and their workflows | Defines capabilities and developer experience |
| Security, regulatory, and SLA constraints | Prevents redesign after implementation |
| Expected change rate in year one and over five years | Selects an evolution strategy |

If the user cannot answer, record explicit assumptions and mark them as open questions. Do not invent
business requirements.

## Workflow

Run the steps in order. Each step has a gate; do not advance while the gate is unmet.

### Step 1. Identify API capabilities (Chapter 2)

Use the questions and canvas in [references/requirements.md](references/requirements.md).

- Convert business goals into capabilities: goal, consumer, inputs, outputs, constraints.
- Keep HTTP methods, URLs, and storage details out of the capability list.
- Group capabilities by business value and confirm them with the user.

**Output:** API Capabilities Canvas.
**Gate:** every capability has a named consumer and a measurable outcome.

### Step 2. Model operations and data (Chapters 3-5)

- For each capability, list operations: create, read, update, delete, batch, long-running.
- Model entities, attributes, identifiers, relationships, and required versus optional data.
- Keep the representation consumer-oriented; it must not mirror the database schema.

**Output:** operation list and data model, independent of API style.
**Gate:** each operation traces to a capability; every entity has an identity and ownership rule.

### Step 3. Represent the contract in HTTP and OpenAPI (Chapters 4, 6-7)

- Assign HTTP methods and status codes according to semantics, safety, and idempotency.
- Express data with JSON Schema and the API with OpenAPI.
- Validate the document with the project's linter before review.

**Output:** valid OpenAPI document plus JSON Schema definitions.
**Gate:** the OpenAPI linter passes and every operation documents success and error responses.

### Step 4. Make the API friendly and interoperable (Chapters 8-11)

- **Data (Ch. 8):** consistent naming, formats, null/optional handling, and one error shape.
- **Operations (Ch. 9):** self-explanatory names, predictable behavior, consistent pagination and filtering.
- **Flows (Ch. 10):** cover create, confirm, read, and update journeys; define partial success for batch work.
- **Whole API (Ch. 11):** consistent concepts, content negotiation, and hypermedia only where it pays off.

**Output:** updated contract and a developer-experience review.
**Gate:** categories B-D of the audit checklist pass.

### Step 5. Address constraints (Chapters 12-14)

- **Security (Ch. 12):** authentication, authorization scopes/roles, data protection, auditability.
- **Efficiency (Ch. 13):** caching, compression, field selection, and pagination where needed.
- **Context (Ch. 14):** network topology, regulatory rules, and environment-specific limits.

**Output:** a decision record per constraint with rationale.
**Gate:** category E of the audit checklist passes; no constraint is deferred without an owner.

### Step 6. Plan evolution and stability (Chapter 15)

Use [references/evolution.md](references/evolution.md).

- Define what counts as a breaking change for this API and its consumers.
- Choose URL, header, or media-type versioning with a written rationale.
- Specify how fields, operations, and deprecations are introduced.

**Output:** API evolution strategy.
**Gate:** category F of the audit checklist passes.

### Step 7. Standardize and automate (Chapters 16-19)

- Write design guidelines as rules with rationale (Ch. 16).
- Add Spectral or equivalent rules to CI (Ch. 18).
- Optimize the OpenAPI document (Ch. 17) and enrich generated artifacts (Ch. 19).

**Output:** guidelines, lint rules, and CI integration.
**Gate:** category G of the audit checklist passes and the rules run on every contract change.

## Reference map

| Need | Read |
| --- | --- |
| Requirements questions, canvas, operation template | [references/requirements.md](references/requirements.md) |
| Design and audit checklist A-G with chapter references | [references/audit-checklist.md](references/audit-checklist.md) |
| Versioning, compatibility, deprecation templates | [references/evolution.md](references/evolution.md) |
| Attribution, chapter map, official examples repository | [references/sources.md](references/sources.md) |

## Audit-only requests

When the user asks to review an existing API rather than design one:

1. Read the OpenAPI document and available guidelines.
2. Apply [references/audit-checklist.md](references/audit-checklist.md) category by category.
3. Report each item as pass, fail, or not applicable, with file/operation evidence.
4. Prioritize findings by consumer impact and compatibility risk.
5. Do not redesign the API unless the user explicitly asks for remediation.

## Boundaries

- Implementation details for ASP.NET Core belong to `dotnet-webapi`.
- C# refactoring, gRPC/protobuf code generation, and infrastructure work are out of scope.
- Do not invent requirements, chapter contents, or book quotations.
- Never include secrets, credentials, or machine-specific absolute paths in artifacts.

## Completion criteria

- The capability canvas, operation/data model, OpenAPI contract, audit results, evolution strategy,
  and guideline set exist at the depth the request requires.
- Every design decision has a rationale and, where relevant, a compatibility classification.
- Checklist categories applicable to the request have an explicit verdict.
- The OpenAPI document is valid and the lint rules are runnable.
