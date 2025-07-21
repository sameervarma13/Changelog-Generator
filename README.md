# LLM Changelog Generator

This project provides a Python-based toolset for generating changelogs using large language models (LLMs). It processes code or text input and produces summaries or changelogs that reflect the changes between versions. The tool is designed for easy testing and integration into workflows involving model evaluation or version tracking.

## Features

- Automatically generate changelogs from diffs or modified text files
- Modular design with a core script (`generate_changelog.py`) and test files for evaluation
- Compatible with Claude and other LLMs (configurable backend)
- Includes sample input files and unit tests

## Repository Structure

```
.
├── generate_changelog.py          # Core script for generating changelogs using an LLM
├── test.txt                       # Sample input file (e.g. file contents for testing)
├── test.ipynb                     # Jupyter notebook for exploratory testing
├── test_claude.py                 # Tests specific to Claude model usage
├── test_generate_changelog.py    # Unit tests for the changelog generation logic
```

## Getting Started

1. **Install dependencies**
   ```
   pip install openai
   ```

2. **Run changelog generator**
   ```bash
   python generate_changelog.py --before before.txt --after after.txt
   ```

3. **Run tests**
   ```bash
   pytest test_generate_changelog.py
   ```

## Usage Notes

- The `generate_changelog.py` script requires access to an LLM API. Ensure your API key is configured via environment variables if required.
- Test files use mocked outputs for predictable results.

## License

MIT License
