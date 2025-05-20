# Tool: make_http_request
# Original callable name might differ if aliased (e.g. vN versions)

def make_http_request_tool(
    url: str,
    method: str = "GET",
    headers: dict = None,
    params: dict = None,
    json_payload: dict = None,
    data_payload=None, # Can be dict for form data, or string
    timeout: int = 10 # Seconds
) -> dict:
    """
    Makes an HTTP request to the specified URL using the given method and options.

    Args:
        url (str): The URL to request.
        method (str, optional): HTTP method (e.g., "GET", "POST", "PUT", "DELETE"). Defaults to "GET".
        headers (dict, optional): Dictionary of HTTP headers.
        params (dict, optional): Dictionary of URL parameters (for GET requests).
        json_payload (dict, optional): JSON data to send in the request body (sets Content-Type to application/json).
        data_payload (any, optional): Data to send in the request body (e.g., for form data).
                           If json_payload is provided, this is ignored.
        timeout (int, optional): Request timeout in seconds. Defaults to 10.

    Returns:
        dict: A dictionary containing:
            'success' (bool): True if the request was successful (2xx status code), False otherwise.
            'status_code' (int or None): HTTP status code, or None if request failed before sending.
            'headers' (dict or None): Response headers as a dictionary, or None.
            'text_content' (str or None): Response body as text if applicable, or None.
            'json_content' (dict or None): Response body parsed as JSON if applicable, or None.
            'error_message' (str or None): Error message if the request failed or an exception occurred.
            'url' (str): The URL that was requested.
    """
    tool_name = "make_http_request_tool"
    print(f"Agent log ({tool_name}): Called with URL='{url}', Method='{method}'.")

    if not _REQUESTS_AVAILABLE:
        msg = "The 'requests' library is not available. Cannot make HTTP requests."
        print(f"Agent log ({tool_name}): {msg}")
        return {
            "success": False, "status_code": None, "headers": None, 
            "text_content": None, "json_content": None, "error_message": msg, "url": url
        }

    method = method.upper()
    response_data = {
        "success": False, "status_code": None, "headers": None,
        "text_content": None, "json_content": None, "error_message": None, "url": url
    }

    try:
        request_kwargs = {"headers": headers or {}, "params": params, "timeout": timeout}
        
        if json_payload is not None:
            request_kwargs["json"] = json_payload
            if "Content-Type" not in request_kwargs["headers"]: # Auto-set if not provided
                 request_kwargs["headers"]["Content-Type"] = "application/json"
        elif data_payload is not None:
            request_kwargs["data"] = data_payload

        print(f"Agent log ({tool_name}): Making {method} request to {url} with args: {request_kwargs}")
        
        response = requests.request(method, url, **request_kwargs)
        
        response_data["status_code"] = response.status_code
        response_data["headers"] = dict(response.headers)
        response_data["text_content"] = response.text
        
        # Try to parse JSON content if Content-Type suggests it
        content_type = response.headers.get("Content-Type", "").lower()
        if "application/json" in content_type:
            try:
                response_data["json_content"] = response.json()
            except json.JSONDecodeError:
                print(f"Agent log ({tool_name}): Content-Type was JSON, but failed to decode JSON response.")
                # Keep text_content available
        
        # Consider 2xx status codes as success
        if 200 <= response.status_code < 300:
            response_data["success"] = True
            print(f"Agent log ({tool_name}): Request successful ({response.status_code}).")
        else:
            response_data["success"] = False
            response_data["error_message"] = f"HTTP Error: {response.status_code} {response.reason}"
            print(f"Agent log ({tool_name}): Request failed ({response.status_code} {response.reason}).")
            print(f"Agent log ({tool_name}): Response text for error: {response.text[:500]}...")


    except requests.exceptions.RequestException as e:
        error_msg = f"RequestException: {type(e).__name__}: {e}"
        print(f"Agent log ({tool_name}): {error_msg}")
        response_data["error_message"] = error_msg
    except Exception as e:
        error_msg = f"Unexpected error during HTTP request: {type(e).__name__}: {e}"
        print(f"Agent log ({tool_name}): {error_msg}")
        response_data["error_message"] = error_msg
        
    return response_data
