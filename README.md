# weekly-ai-briefing

Use Claude to generate a high information density weekly briefing

## Kokoro model files

`email_briefing` voices each section locally with [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx), so no
network or API key is needed for text-to-speech. The model files (about 190 MB) are not in git. Download them once
from the repository root:

```sh
mkdir models
curl -L -o models/kokoro-v1.0.fp16.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.fp16.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
```

The voice is set by `VOICE` in `src/weekly_ai_briefing/config.py`; any voice in `voices-v1.0.bin` works.

Other text-to-speech backends (OpenVINO GenAI on the Arc GPU and NPU, Qwen3-TTS) were benchmarked and did not beat
this CPU setup; see [documents/model_selection.md](documents/model_selection.md).

## Publishing

The mp3 files are too large to commit, so they are uploaded as assets of one GitHub release per edition
(tag `ai-outlook-briefing-<date>`). GitHub Pages serves `index.html` and `editions/html_format/`, whose pages play
the mp3s from those release assets. The weekly email is a single message linking to the edition's page, not the
audio. One-time setup: install the [GitHub CLI](https://cli.github.com/) (`winget install GitHub.cli`) and run
`gh auth login`. Each week, after the briefing text is generated:

```powershell
.\scripts\publish_text.ps1
```

The script waits for the edition page to return HTTP 200 before sending the email (up to 10 minutes). If that
times out, rerun `uv run python -m weekly_ai_briefing.email_briefing --email` once the page is live.
`--voice --section N` voices only some sections. `publish --date YYYY-MM-DD` publishes an older edition;
`publish --no-upload` only rebuilds the pages.
