import requests

BASE_URL = "http://127.0.0.1:8000"


def main():
    # Health check
    health = requests.get(f"{BASE_URL}/health", timeout=20)
    print("HEALTH:", health.status_code, health.json())

    # Query test
    payload = {
        "question": "What is the standard duration of the Master’s program?"
    }

    r = requests.post(f"{BASE_URL}/query", json=payload, timeout=180)
    print("\nQUERY STATUS:", r.status_code)

    data = r.json()
    print("\nANSWER:\n", data.get("answer", ""))

    print("\nSOURCES:")
    for s in data.get("sources", []):
        print("-", s)


if __name__ == "__main__":
    main()
