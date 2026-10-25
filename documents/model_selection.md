# Model selection: why CPU and not the Intel GPU

Evaluated on a Core Ultra 7 258V (Lunar Lake) with an Arc 140V iGPU and NPU, switching to Intel's OpenVINO GenAI
`Text2SpeechPipeline` (`OpenVINO/Kokoro-82M-*-ov` models). It did not beat the current `kokoro-onnx` + `onnxruntime`
CPU path, so we kept it. Same ~1,600-character chunk, voice `af_heart`.

RTF (real-time factor) is synthesis wall-clock time divided by the duration of the audio produced. Lower is better:
0.25 means 25 s of compute for 100 s of audio (4x faster than real time), and 1.0 or more means synthesis takes as
long as the audio plays, or longer.

| Path | Wall time / audio | RTF |
| --- | --- | --- |
| **kokoro-onnx, ORT CPU, fp16 (current)** | 25.7 s / 102 s | **0.25** |
| OpenVINO GenAI, CPU, int8 | 36.9 s / 99 s | 0.37 |
| OpenVINO GenAI, Arc GPU, int8 | 127 s first call, then 20.2 s / 99 s | 1.29, then 0.205 |
| OpenVINO GenAI, Arc GPU, fp16 | 97, 46, 11.5, 45 s for four different texts | 0.98, 0.55, 0.20, 0.45 |
| OpenVINO GenAI, NPU, int8 | crashed: `ZE_RESULT_ERROR_DEVICE_LOST` | n/a |
| Qwen3-TTS 0.6B CustomVoice, OpenVINO GenAI, CPU, default export | 307 s / 112 s, then 398 s / 144 s | 2.74, 2.77 |
| Qwen3-TTS 0.6B CustomVoice, OpenVINO GenAI, Arc GPU, default export | 195 s / 149 s, then 167 s / 129 s | 1.31, 1.29 |

- The GPU is only ~20% faster than the CPU in its best case, and only when the input shape repeats. Kokoro's input
  shape varies per chunk and each new shape appears to trigger a slow GPU recompile (inferred from timings, not
  confirmed in logs), so a real briefing would likely be slower on the GPU.
- The NPU is unusable with Kokoro on the current driver.
- Qwen3-TTS (`Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`, speaker `ryan`, same text) is about 5x (GPU) to 11x (CPU) slower
  than the current Kokoro CPU path, and slower than real time on both. "Default export" means
  `optimum-cli export openvino --trust-remote-code` with no weight-format option. It needs a local export (no
  preconverted OpenVINO models exist), Python 3.12 and the nightly `openvino-genai` (2026.5 dev); the released
  2026.4.1 rejects the export. Audio length varies run to run for identical text (112 to 149 s), so the RTF figures
  are approximate. Voice quality was not evaluated, and it has no `af_heart` equivalent: its voices are a fixed list.
- `onnxruntime-openvino` has Windows wheels only for Python 3.11 to 3.13 (latest 1.24.1); this project uses 3.14 and
  `onnxruntime>=1.31`. It was not benchmarked.
- `magicunicorn/kokoro-tts-intel` is a third-party repackaging of Kokoro v0.19 pinned to `onnxruntime-openvino==1.17.0`,
  benchmarked on an older Iris Xe iGPU, and lacks the v1.0 voices. Not considered.
- Revisit if the GPU path gets fixed-shape chunking plus a compile cache (`CACHE_DIR`), or if CPU voicing time becomes
  a problem. Untested CPU options: ORT `intra_op_num_threads` tuning and the int8 kokoro-onnx model.

## Python version

The project stays on Python 3.14 (`requires-python = ">=3.14"`). The current stack, `kokoro-onnx` and `onnxruntime`
1.31, runs on it, and every Python constraint that came up belonged to a backend rejected above:

- `onnxruntime-openvino` has Windows wheels only for 3.11 to 3.13.
- Exporting Qwen3-TTS needed 3.12 (pinned `torch==2.11.0` and `transformers==4.57.3`).
- Exporting Kokoro locally (`kokoro` and `misaki` packages) needs Python below 3.13. The preconverted
  `OpenVINO/Kokoro-82M-*-ov` models avoid that, and `openvino-genai` has cp314 wheels.

Revisit only if a backend that is worth adopting ships wheels for older Python versions only. For a one-off model
export, use a throwaway 3.12 environment instead of changing the project's version. A future dependency lacking a
3.14 wheel would also be a reason to pin back.
