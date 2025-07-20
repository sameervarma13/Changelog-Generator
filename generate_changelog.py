import subprocess
import requests
import json
import argparse
import sys
import os

# Mintlify Claude API Proxy Configuration
API_KEY = ""
BASE_URL = "https://mintlify-take-home.com"
ENDPOINT = "/api/message"
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_git_commits(n):
    """Fetch the last `n` commits from the git log."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{n}", "--pretty=format:%h %s"],
            capture_output=True,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split("\n")
        if not commits:
            print("No commits found. Ensure you're in a Git repository and have commit history.")
            sys.exit(1)
        return commits
    except subprocess.CalledProcessError:
        print("Error: This script must be run inside a Git repository.")
        sys.exit(1)

# def get_mock_git_commits(n):
#     """ returns mock commit data instead of running Git CLI."""
#     print("Using mock commit data instead of git log")
#     commits = [
#         "Fixed issue where code snippets were not rendering properly in certain browsers.",
#         "Added AI-powered autocomplete for documentation searches.",
#         "Optimized caching strategy to minimize redundant API calls and improve responsiveness.",
#         "Implemented Markdown (.md) export for documentation pages.",
#         "Updated README with clearer setup instructions for new users.",
#         "Refactored database schema to improve query performance and reduce load times by 40%.",
#         "Fixed UI glitch where dropdown menus were not closing after selection.",
#         "Resolved an authentication issue preventing certain users from logging in.",
#         "Introduced new 'Analytics Dashboard' to track documentation usage metrics.",
#         "Expanded API documentation with additional code examples and best practices.",
#         "Redesigned API Playground UI for a more intuitive user experience.",
#         "Enabled real-time collaboration for editing documentation with multiple users.",
#         "Fixed broken links in auto-generated API documentation.",
#         "Added support for dark mode in the documentation editor.",
#         "Improved accessibility support by adding screen reader compatibility for visually impaired users.",
#         "Resolved a bug causing slow API responses under high traffic conditions.",
#         "Updated search ranking algorithm to return more relevant documentation results.",
#         "Improved consistency of documentation structure for better navigation.",
#         "Clarified error-handling guidelines in API documentation.",
#         "Added tutorial on integrating third-party authentication providers with the platform."
#     ][:n]  # Return exactly `n` commits

#     print("\n[DEBUG] Returning the following commits:", commits)  # Debug print
#     return commits



def generate_changelog_payload(commits):
    """Formats commit messages into a API request payload."""

    # print("\n[DEBUG] Received commits for payload:", commits)  # Debug print

    commit_log = "\n".join(commits)  # combining all commits
    
    #scaling token limit according to the number of commits
    max_tokens = min(2000, 500 + len(commits) * 5) 

    prompt = (
        "Generate a concise changelog summarizing the following git commit messages. "
        "Focus on grouping related changes together, avoiding unnecessary details, and keeping the summary brief. "
        "Ensure the changelog is structured with clear sections like:\n"
        "- **New Features** (Major additions users should know about)\n"
        "- **Improvements** (Performance, UI, or usability enhancements)\n"
        "- **Bug Fixes** (Resolved issues and stability fixes)\n"
        "- **Other Updates** (Anything else that is relevant but not critical)\n\n"
        "Summarize multiple small commits into a single bullet point if they are related, and do not list every commit separately. "
        "The goal is to keep the changelog short and readable.\n\n"
        "Return **only the formatted changelog**, with no introductions or explanations. Do not include phrases like 'Here's a concise changelog' or additional notes at the end.\n\n"
        "### Commits to process:\n\n"
        f"{commit_log}"
    )

    payload = {
        "model": "claude-3-5-sonnet-latest",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.5
    }

    # print("\n[DEBUG] Payload Generated:\n", json.dumps(payload, indent=2))  # Debug print
    return payload

def call_mintlify_api(payload):
    """Sends the formatted request to Mintlify’s proxy API."""
    url = BASE_URL + ENDPOINT
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: API request failed with status {response.status_code}")
        print(response.text)
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate a changelog from git commits using Mintlify’s Claude API proxy.")
    parser.add_argument("n", type=int, help="Number of commits to include in the changelog.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    commits = get_git_commits(args.n)
   
    payload = generate_changelog_payload(commits)
    response = call_mintlify_api(payload)

    if response:
        print((response["content"][0]['text']))

def install_as_cli():
    """Installs the script as a CLI tool in the user's local bin directory."""
    script_path = os.path.abspath(__file__)
    install_path = os.path.expanduser("~/.local/bin/generate-changelog")

    print(f"\n[INSTALLING] Copying script to {install_path}...")

    os.makedirs(os.path.dirname(install_path), exist_ok=True)
    with open(script_path, "r") as src, open(install_path, "w") as dest:
        dest.write(src.read())

    os.chmod(install_path, 0o755)  # Make it executable
    print(f"\nInstallation is complete! You can now run it using:\n  generate-changelog 5")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_as_cli()
        sys.exit(0)

    if not os.path.exists("~/.local/bin/generate-changelog"):
        print("\n[INFO] To install as a CLI tool, run: python generate_changelog.py --install\n")

    main()


