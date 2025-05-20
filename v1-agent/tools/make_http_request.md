# Tool: make_http_request

**Description:**
Makes HTTP requests (GET, POST, etc.). Handles headers, params, JSON/data payloads, and timeout. Returns status, headers, and content (text/JSON).

**Signature:**
```python
make_http_request(url: str, method: str = 'GET', headers: dict = None, params: dict = None, json_payload: dict = None, data_payload=None, timeout: int = 10) -> dict
```
