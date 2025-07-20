import unittest
from unittest.mock import patch, MagicMock
import json
from generate_changelog import get_git_commits, generate_changelog_payload, call_mintlify_api

class TestGitLogExtraction(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_git_commits(self, mock_subprocess):
        """Test that git commits are correctly extracted from git log."""
        mock_subprocess.return_value.stdout = "abcd123 Fix bug\nxyz789 Add feature"
        commits = get_git_commits(2)
        
        expected_commits = ["abcd123 Fix bug", "xyz789 Add feature"]
        self.assertEqual(commits, expected_commits)

    @patch("subprocess.run")
    def test_get_git_commits_empty(self, mock_subprocess):
        """Test handling when no commits are returned."""
        mock_subprocess.return_value.stdout = ""
        commits = get_git_commits(2)
        
        self.assertEqual(commits, [])

class TestChangelogPayload(unittest.TestCase):
    def test_generate_changelog_payload(self):
        """Test that the API payload is correctly formatted."""
        commits = ["abcd123 Fix bug", "xyz789 Add feature"]
        payload = generate_changelog_payload(commits)
        
        self.assertEqual(payload["model"], "claude-3-5-sonnet-latest")
        self.assertEqual(payload["max_tokens"], 4096)
        self.assertEqual(payload["temperature"], 0.5)
        self.assertIn("Fix bug", payload["messages"][0]["content"])
        self.assertIn("Add feature", payload["messages"][0]["content"])

class TestMintlifyAPI(unittest.TestCase):
    @patch("requests.post")
    def test_call_mintlify_api_success(self, mock_post):
        """Test successful API response handling."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "messages": [{"role": "assistant", "content": "Generated changelog"}]
        }
        mock_post.return_value = mock_response

        payload = generate_changelog_payload(["abcd123 Fix bug"])
        response = call_mintlify_api(payload)

        self.assertEqual(response, {"messages": [{"role": "assistant", "content": "Generated changelog"}]})

    @patch("requests.post")
    def test_call_mintlify_api_failure(self, mock_post):
        """Test API failure handling."""
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        payload = generate_changelog_payload(["abcd123 Fix bug"])
        response = call_mintlify_api(payload)

        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()
