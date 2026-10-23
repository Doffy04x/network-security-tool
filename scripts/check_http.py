"""Check the real HTTP path through NGINX, on the local CI runner only."""

import json
import sys
import urllib.error
import urllib.request

def request(base, path, expected_status):
    try:
        with urllib.request.urlopen(base + path, timeout=5) as response:
            status, payload = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, payload = error.code, error.read()
    assert status == expected_status, (path, status, payload)
    data = json.loads(payload)
    print(json.dumps({"path": path, "status": status, "response": data}))
    return data


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080"
    if not base.startswith("http://127.0.0.1:"):
        raise SystemExit("Use the local runner's loopback address")
    assert request(base, "/health", 200) == {"status": "ok"}
    assert request(base, "/api/check?port=8000", 200) == {"host": "127.0.0.1", "port": 8000, "open": True}
    for path in ["/api/check?port=70000", "/api/check?port=0", "/api/check?port=abc", "/api/check", "/api/check?port=80&port=443", "/api/check?port=80&host=example.com"]:
        request(base, path, 400)
    request(base, "/not-found", 404)
    print("NGINX -> API communication and input checks passed")


if __name__ == "__main__":
    main()
