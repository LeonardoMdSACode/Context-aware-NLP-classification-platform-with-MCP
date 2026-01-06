## Pydantic / FastAPI deprecations

- Migrate BaseSettings Config → ConfigDict
- Replace Field(example=...) with json_schema_extra
- Replace @app.on_event with lifespan handler

Status: deferred (non-blocking)
