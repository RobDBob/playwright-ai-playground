# Playwright AI Playground

A small Python browser-automation project using UV, pytest, Playwright, and an
optional local Ollama model. The example tests submit the public Practice Test
Automation login form with valid and invalid demo credentials.

## Requirements

- Python 3.11 or newer
- [UV](https://docs.astral.sh/uv/)
- Google Chrome (the tests explicitly use the Chrome browser channel)
- [Ollama](https://ollama.com/) only if you want AI-generated test summaries

## Project layout

```text
.
├── scripts/
│   └── ollama_test_runner.py
├── tests/
│   ├── conftest.py
│   └── test_practice_login.py
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Setup with UV

From the project directory:

1. Install UV using the instructions for your operating system at
   <https://docs.astral.sh/uv/getting-started/installation/>.
2. Create the project environment and install Python dependencies:

   ```sh
   uv sync
   ```

3. Install Playwright's Chrome channel:

   ```sh
   uv run playwright install chrome
   ```

   On Linux, if the browser reports missing operating-system libraries, install
   them with `uv run playwright install-deps chromium` (or use your
   distribution's package manager).

  alternatively, install chrome manually - linux mint instructions
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  sudo add-apt-repository "deb http://dl.google.com/linux/chrome/deb/ stable main"
  sudo apt update
  sudo apt install google-chrome-stable

4. Run the tests:

   ```sh
   uv run pytest
   ```

Pytest is configured to launch Google Chrome by default.

## Install and run manually without UV

Create and activate a virtual environment using your preferred Python
environment tool, then run:

```sh
python -m pip install -r requirements.txt
python -m playwright install chrome
python -m pytest
```

The pytest configuration in `pyproject.toml` selects the Chrome channel for
this manual workflow too.

## Login test configuration

The demo site publishes `student` / `Password123` as its test credentials; the
tests use those values by default. Override the URL or credentials with
environment variables when needed. Do not commit real credentials.

Linux/macOS:

```sh
export PRACTICE_LOGIN_URL="https://practicetestautomation.com/practice-test-login/"
export PRACTICE_USERNAME="student"
export PRACTICE_PASSWORD="Password123"
uv run pytest
```

PowerShell:

```powershell
$env:PRACTICE_LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"
$env:PRACTICE_USERNAME = "student"
$env:PRACTICE_PASSWORD = "Password123"
uv run pytest
```

The tests cover successful login and rejection of an invalid username or
password. They navigate to the public site, so the machine needs network access.

## Optional Ollama test runner

Install Ollama from <https://ollama.com/download>, start its local service, and
download a model (the default below is `llama3.2`):

```sh
ollama pull llama3.2
```

Run pytest and ask that local model to summarize the captured test output:

```sh
uv run python scripts/ollama_test_runner.py
```

Choose another locally installed model with `--model` or the `OLLAMA_MODEL`
environment variable:

```sh
uv run python scripts/ollama_test_runner.py --model llama3.2 -k invalid
```

The test runner returns pytest's exit code. Ollama must be running locally and
the selected model must already be available; Ollama connectivity or model
errors are reported by the client.

## Troubleshooting

- **`uv` is not recognized:** install UV and open a new terminal, then check
  `uv --version`.
- **Chrome executable not found:** run `uv run playwright install chrome`
  after `uv sync`. For the manual setup, run `python -m playwright install
  chrome` in the active environment.
- **Linux reports missing shared libraries:** run
  `uv run playwright install-deps chromium` with the required system
  permissions, or install the missing libraries through your Linux
  distribution.
- **Browser starts but the page does not load:** check network access, proxy
  settings, and whether the demo site is available.
- **Login assertion fails:** confirm the demo credentials and check whether the
  site's login page or expected messages have changed. Override credentials
  with `PRACTICE_USERNAME` and `PRACTICE_PASSWORD` if the site changes them.
- **Ollama connection error:** start the Ollama service, verify
  `ollama list` shows the selected model, and retry. Ollama is only needed for
  the optional summary runner; `uv run pytest` does not use it.
- **Need more pytest detail:** run `uv run pytest -vv --headed` to show the
  browser while tests execute, or add `--tracing on` to save Playwright traces.
