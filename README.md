# AI Security Scanner

A small command-line prototype that sends a source file to an Ollama model and prints AI-generated security findings.

## Requirements

- Python 3.12 or newer
- [Ollama](https://ollama.com/) installed and running
- The `qwen2.5:7b` model

## Setup

Pull the model and install the Python dependencies:

```bash
ollama pull qwen2.5:7b
python -m pip install ollama requests
```

## Usage

```bash
python scanner.py path/to/source-file
```

The scanner reads the entire file and sends its contents to the Ollama host. By default, that host is `http://localhost:11434`. Set `API_HOST` in the process environment to configure the Ollama client:

```bash
API_HOST=http://localhost:11434 python scanner.py path/to/source-file
```

The availability check currently targets `localhost:11434` directly, so configuring a remote `API_HOST` may not work correctly. The scanner also sends an `x-some-header` header; `HEADER_VALUE` controls its value and defaults to a placeholder.

## Limitations

This is an experimental aid, not a comprehensive security audit. Model output can be incomplete or incorrect; review findings independently. Avoid sending confidential source code to a remote Ollama host unless you are authorized to do so and the connection is appropriately protected.

## License

No license is included yet. Add one before publishing if you want to grant others permission to reuse or distribute the project.
