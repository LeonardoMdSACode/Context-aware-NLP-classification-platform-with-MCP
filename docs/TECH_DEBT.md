## Pydantic / FastAPI deprecations

- Migrate BaseSettings `Config` → `ConfigDict`
- Replace `Field(example=...)` with `json_schema_extra`
- `datetime.utcnow()` usage in logging → switch to timezone-aware `datetime.now(datetime.UTC)`

Status: deferred (non-blocking)
