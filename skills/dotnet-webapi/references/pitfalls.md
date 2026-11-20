# Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Exposing domain entities as API responses | Create separate `sealed record` request/response types. Entities leak navigation properties and internal fields. |
| Forgetting `CancellationToken` | Add to every endpoint and forward through the entire async call chain. |
| Returning `200 OK` from POST create | Return `201 Created` with a `Location` header. |
| Missing OpenAPI metadata | Chain `.WithName()`, `.WithSummary()`, `.WithDescription()`, `.Produces<T>()` on every endpoint. |
| Injecting data stores directly into endpoints | Use a service layer with an interface for separation and testability. |
| Mixing controller and minimal API styles | Pick one per project and be consistent. |
| `TypedResults` in ternary without explicit return type | `Ok<T>` and `NotFound` have no common base — annotate with `Task<Results<Ok<T>, NotFound>>` or fall back to `Results` factory. |
| Using mutable classes for DTOs | Use `sealed record` with positional syntax (responses) or `init` properties (requests). |
| Registering services without interfaces | Define `IService` and register with `AddScoped<IService, Service>()`. |
| Adding any `Swashbuckle.*` package to new .NET 9+ projects | Use built-in `AddOpenApi()` + `MapOpenApi()`. Do not add `Swashbuckle.AspNetCore`, `Swashbuckle.AspNetCore.SwaggerUI`, or any other Swashbuckle package. |
| Missing XML doc comments on DTOs | Add `<summary>` XML doc comments to every request and response type. These flow into the generated OpenAPI spec automatically. |
| Using `DateTime` for date/time properties | Use `DateTimeOffset` instead — it preserves UTC offset, avoids timezone ambiguity, and serializes correctly in JSON. |
| Serializing enums as integers | Configure `JsonStringEnumConverter` so enums serialize as strings by default. Only use integer serialization if the user explicitly requests it. |
