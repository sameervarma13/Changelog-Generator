import requests
import json

# Replace with your actual Mintlify API key
API_KEY = ""

BASE_URL = "https://mintlify-take-home.com"
ENDPOINT = "/api/message"
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Dummy commit data
dummy_commits = [
    "abcd123 Fixed login issue",
    "efgh456 Improved database query performance",
    "ijkl789 Refactored authentication logic"
]

# Create a test payload
test_payload = {
    "model": "claude-3-5-sonnet-latest",
    "messages": [
        {
            "role": "user",
            "content": f"Based on the following git commit messages, generate a changelog that is clear and user-friendly:\n\n{chr(10).join(dummy_commits)}"
        }
    ],
    "max_tokens": 4096,
    "temperature": 0.5
}

def test_claude_api():
    """Send a request to Mintlify’s Claude API Proxy with dummy data."""
    url = BASE_URL + ENDPOINT
    response = requests.post(url, headers=HEADERS, json=test_payload)

    print("\n[DEBUG] API Response Status:", response.status_code)
    print("\n[DEBUG] Raw API Response:\n", response.text)

    if response.status_code == 200:
        data = response.json()
        print("\n[RESULT] Generated Changelog:\n", content = data.get("content", []))
    else:
        print("\n[ERROR] API request failed.")

if __name__ == "__main__":
    test_claude_api()
