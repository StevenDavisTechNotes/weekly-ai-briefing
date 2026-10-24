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
