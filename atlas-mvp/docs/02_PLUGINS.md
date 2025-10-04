# Building Atlas Plugins

Plugins let you extend Atlas with local tools. Each plugin lives in its own folder under `plugins/` with two required files:

1. `manifest.yaml`
2. Python module exposing `run(payload)`

## Example layout

```
plugins/example_tool/
  manifest.yaml
  example_tool.py
  README.md
```

## Manifest fields

```yaml
name: Example Tool
entrypoint: example_tool.py
description: Summarises a local file.
```

* `name` — Human friendly name shown in the UI.
* `entrypoint` — Relative path to the Python module that contains `run(payload)`.
* `description` — Helpful summary.

## Writing `run(payload)`

```python
def run(payload: dict) -> dict:
    """Return anything JSON serialisable."""
    text = Path(payload["path"]).read_text()
    return {"length": len(text)}
```

* The function receives a dictionary from the UI.
* It can access local files, call APIs, etc. (keep security in mind).
* Return serialisable data; the UI will render it.

## Enabling plugins

1. Visit the **Plugins** page in Streamlit.
2. Toggle the plugin on.
3. Provide a JSON payload and click **Execute**.

The API stores enable/disable state in SQLite so your preferences persist between sessions.
