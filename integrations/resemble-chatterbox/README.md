# Chatterbox TTS Integration

Open-source text-to-speech integration for OpenClaw using [Resemble AI's Chatterbox](https://www.resemble.ai/chatterbox) - the leading family of open source AI voice models.

## Features

- 🎙️ **High-quality TTS** - Zero-shot voice cloning with 5 seconds of audio
- 🎭 **Emotion control** - Adjust expressiveness from monotone (0.0) to dramatic (2.0)
- 🌍 **Multilingual** - 23+ languages supported
- ⚡ **Fast inference** - ~200ms latency, faster than real-time
- 🔒 **On-premise** - Full control with local deployment
- 💰 **Free forever** - MIT licensed, no usage limits

## Quick Start

### 1. Installation

```bash
cd integrations/resemble-chatterbox
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install PyTorch, Transformers, and dependencies
- Check for GPU support
- Set up output directories

### 2. Activate Environment

```bash
source venv/bin/activate
```

### 3. Run Test

```bash
python chatterbox_tts.py
```

## Usage

### Basic TTS

```python
from chatterbox_tts import ChatterboxTTS

tts = ChatterboxTTS()

# Generate speech
audio = tts.generate("Hello, this is a test.")

# Save to file
tts.save_audio(audio, "output.wav")
```

### Emotion Control

```python
# Monotone delivery
audio = tts.generate("This is important.", emotion_scale=0.0)

# Expressive delivery
audio = tts.generate("This is important!", emotion_scale=1.5)

# Available presets
presets = tts.get_emotion_presets()
# {'monotone': 0.0, 'neutral': 0.5, 'expressive': 1.0, 'dramatic': 1.5}
```

### Voice Cloning

```python
# Clone a voice from reference audio (5+ seconds)
tts.clone_voice(
    reference_audio_path="reference.wav",
    voice_name="my_voice",
    transcript="Reference audio transcript"
)

# Use cloned voice
audio = tts.generate_with_cloned_voice(
    "This uses my cloned voice!",
    voice_name="my_voice"
)
```

### Multilingual

```python
# Generate in different languages
audio = tts.generate("Hello!", language="en")   # English
audio = tts.generate("¡Hola!", language="es")   # Spanish
audio = tts.generate("Bonjour!", language="fr") # French
audio = tts.generate("Hallo!", language="de")   # German
```

## OpenClaw Integration

### Tool Interface

```python
from openclaw_tool import OpenClawChatterboxTool

tool = OpenClawChatterboxTool()
tool.initialize()

# Generate speech
result = tool.generate_speech({
    "text": "Hello from OpenClaw!",
    "emotion": 1.0,
    "output_format": "base64"
})

# Returns base64-encoded audio
audio_b64 = result["audio_base64"]
```

### CLI Usage

```bash
# Generate speech
python openclaw_tool.py generate '{"text": "Hello world"}'

# Clone voice
python openclaw_tool.py clone '{"audio_path": "ref.wav", "voice_name": "my_voice"}'

# List voices
python openclaw_tool.py list_voices

# Health check
python openclaw_tool.py health
```

## Configuration

```python
from chatterbox_tts import ChatterboxConfig, ChatterboxTTS

config = ChatterboxConfig(
    model_name="resemble/chatterbox-0.5b",  # or 1b for higher quality
    device="cuda",  # or "cpu"
    emotion_scale=1.0,
    language="en",
    sample_rate=24000
)

tts = ChatterboxTTS(config)
```

## API Fallback

If local model loading fails, the integration can fall back to Resemble AI's cloud API:

```bash
export RESEMBLE_API_KEY="your_api_key"
```

Get an API key at: https://www.resemble.ai/

## Model Information

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| chatterbox-0.5b | 500M params | Excellent | ~200ms |
| chatterbox-1b | 1B params | Superior | ~300ms |

Models are downloaded automatically on first use (~2-3GB) and cached in `~/.cache/huggingface/`.

## Comparison with Other TTS

| Feature | Chatterbox | ElevenLabs | OpenAI TTS |
|---------|------------|------------|------------|
| Open Source | ✅ MIT | ❌ Closed | ❌ Closed |
| Voice Cloning | ✅ Zero-shot | ✅ Premium | ❌ None |
| Emotion Control | ✅ Unique | ⚠️ Limited | ❌ None |
| On-Premise | ✅ Full | ❌ Cloud | ❌ Cloud |
| Cost | ✅ Free | $0.15/1K chars | $15/1M chars |

## Examples

See `examples.py` for comprehensive usage patterns:

```bash
python examples.py
```

## Requirements

- Python 3.8+
- 8GB+ RAM (16GB recommended)
- GPU optional (CUDA for faster inference)
- ~5GB disk space for models

## File Structure

```
resemble-chatterbox/
├── chatterbox_tts.py      # Core TTS implementation
├── openclaw_tool.py       # OpenClaw tool interface
├── requirements.txt       # Python dependencies
├── setup.sh              # Installation script
├── examples.py           # Usage examples
├── output/               # Generated audio output
└── voices/               # Voice cloning references
```

## Troubleshooting

### Model Download Issues

If model download fails, manually download from Hugging Face:
```bash
huggingface-cli download resemble/chatterbox-0.5b
```

### CUDA Out of Memory

Use CPU mode or reduce batch size:
```python
config = ChatterboxConfig(device="cpu")
```

### Audio Quality Issues

- Ensure reference audio is clear (no background noise)
- Use 5-10 seconds of speech for voice cloning
- Adjust emotion_scale for desired expressiveness

## Resources

- [Chatterbox GitHub](https://github.com/resemble-ai/chatterbox)
- [Resemble AI](https://www.resemble.ai/)
- [Hugging Face Model](https://huggingface.co/resemble/chatterbox-0.5b)

## License

MIT License - Chatterbox is open source and free to use.
