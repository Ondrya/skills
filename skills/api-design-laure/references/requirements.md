# Requirements and Capability Modeling

Use this reference during Step 1 and Step 2 of the skill.

## Requirement analysis questions

Ask these before proposing any endpoint, method, or payload.

| # | Question | Purpose |
| --- | --- | --- |
| 1.1 | What business problem does the API solve? | Separate the goal from the technical means |
| 1.2 | Who are the consumers: internal teams, partners, public clients? | Set documentation, stability, and review rigor |
| 1.3 | What actions must consumers be able to perform? | Build the capability list |
| 1.4 | What data is required as input and produced as output for each action? | Start data modeling |
| 1.5 | What constraints exist: security, regulation, SLA, performance? | Account for constraints early |
| 1.6 | How often will the API change in the first year and over the next five years? | Choose a versioning strategy |

## API Capabilities Canvas

Fill one canvas per capability. Do not include HTTP methods or URLs.

```markdown
### Capability: <name>

- **Consumer:** <who uses it>
- **Goal:** <what they need to accomplish>
- **Input data:** <entities and attributes>
- **Output data:** <result and its meaning>
- **Constraints:** <security, performance, regulatory, SLA>
- **Success measure:** <observable outcome>
```

Quality checks:

- The capability describes value, not a resource or endpoint.
- Each capability has exactly one primary consumer group.
- Inputs and outputs use consumer vocabulary, not table or column names.
- Overlapping capabilities are merged or their boundary is stated.

## Operation specification template

Use this for every operation derived from a capability.

```markdown
### Operation: <verb + entity>

- **Capability:** <link to the canvas>
- **Type:** create | read | update | delete | batch | long-running
- **Consumer intent:** <what the caller is trying to achieve>
- **Input:** <fields, required/optional, validation rules>
- **Output:** <fields, status codes, error cases>
- **Idempotent:** yes | no - <rationale>
- **Authorization:** <scope, role, ownership rule>
- **Open questions:** <unresolved decisions>
```

## Modeling questions

### Operations (Chapter 3)

- Which operations does each capability require: CRUD, batch, long-running, or a custom action?
- Which operations must be idempotent or safely retryable?
- Does partial success need to be represented, or must a batch fail as a unit?
- Is any operation long-running enough to need a job resource and polling or notification?

### Data (Chapter 5)

- Which entities exist, and what identifies each one?
- Which relationships are navigable by consumers, and which stay internal?
- Which attributes are required, optional, nullable, or read-only?
- Which values are enums, free text, or controlled vocabularies?
- Does the model expose internal identifiers or database structure that consumers should not depend on?

### Representation (Chapters 4, 6-7)

- Does each HTTP method match the operation's safety and idempotency?
- Are success and error status codes sufficient for every outcome?
- Is the JSON Schema accurate about required fields, formats, and nullability?
- Can the OpenAPI document be validated and linted without warnings that are silently ignored?
