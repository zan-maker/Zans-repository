#!/usr/bin/env python3
"""
Chatterbox TTS Usage Examples
Resemble AI Open Source Voice AI
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from chatterbox_tts import ChatterboxTTS, ChatterboxConfig
import torchaudio


def example_1_basic_tts():
    """Example 1: Basic text-to-speech"""
    print("\n" + "="*60)
    print("Example 1: Basic Text-to-Speech")
    print("="*60)
    
    # Initialize with default settings
    tts = ChatterboxTTS()
    
    # Simple generation
    text = "Hello! I'm Chatterbox, an open source text to speech model."
    audio = tts.generate(text)
    
    # Save to file
    tts.save_audio(audio, "output/example1_basic.wav")
    print(f"✅ Generated: {text}")


def example_2_emotion_control():
    """Example 2: Emotion exaggeration control"""
    print("\n" + "="*60)
    print("Example 2: Emotion Control")
    print("="*60)
    
    tts = ChatterboxTTS()
    text = "This is absolutely incredible! I can't believe how well this works."
    
    emotions = {
        "monotone": 0.0,
        "neutral": 0.5,
        "expressive": 1.0,
        "dramatic": 1.5
    }
    
    for emotion_name, scale in emotions.items():
        print(f"\nGenerating with {emotion_name} (scale={scale})...")
        audio = tts.generate(text, emotion_scale=scale)
        tts.save_audio(audio, f"output/example2_{emotion_name}.wav")


def example_3_multilingual():
    """Example 3: Multilingual TTS"""
    print("\n" + "="*60)
    print("Example 3: Multilingual Support")
    print("="*60)
    
    tts = ChatterboxTTS()
    
    # Test different languages
    phrases = {
        "en": "Hello, how are you today?",
        "es": "¡Hola! ¿Cómo estás hoy?",
        "fr": "Bonjour! Comment allez-vous?",
        "de": "Guten Tag! Wie geht es Ihnen?"
    }
    
    for lang, text in phrases.items():
        print(f"\nGenerating {lang}: {text}")
        audio = tts.generate(text, language=lang)
        tts.save_audio(audio, f"output/example3_{lang}.wav")


def example_4_voice_cloning():
    """Example 4: Voice cloning with reference audio"""
    print("\n" + "="*60)
    print("Example 4: Voice Cloning")
    print("="*60)
    
    tts = ChatterboxTTS()
    
    # Note: You need a reference audio file for this
    reference_audio = "voices/reference_sample.wav"
    
    if not Path(reference_audio).exists():
        print(f"⚠️ Reference audio not found: {reference_audio}")
        print("   Create a 5-10 second audio clip of clear speech")
        print("   and save it to voices/reference_sample.wav")
        return
    
    # Clone the voice
    success = tts.clone_voice(
        reference_audio_path=reference_audio,
        voice_name="my_cloned_voice",
        transcript="This is the reference transcript for voice cloning."
    )
    
    if success:
        # Generate speech with cloned voice
        text = "This is me speaking with my cloned voice!"
        audio = tts.generate_with_cloned_voice(text, voice_name="my_cloned_voice")
        tts.save_audio(audio, "output/example4_cloned.wav")


def example_5_batch_generation():
    """Example 5: Batch processing multiple texts"""
    print("\n" + "="*60)
    print("Example 5: Batch Generation")
    print("="*60)
    
    tts = ChatterboxTTS()
    
    texts = [
        "Welcome to our presentation.",
        "Today we'll discuss the quarterly results.",
        "Revenue increased by fifteen percent.",
        "Questions will be taken at the end."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\nGenerating {i}/{len(texts)}: {text}")
        audio = tts.generate(text, emotion_scale=0.8)
        tts.save_audio(audio, f"output/example5_batch_{i:02d}.wav")


def example_6_openclaw_integration():
    """Example 6: Using via OpenClaw tool interface"""
    print("\n" + "="*60)
    print("Example 6: OpenClaw Tool Integration")
    print("="*60)
    
    from openclaw_tool import OpenClawChatterboxTool
    
    # Initialize tool
    tool = OpenClawChatterboxTool()
    result = tool.initialize({"emotion_scale": 1.0})
    print(f"Initialization: {result}")
    
    # Generate speech
    params = {
        "text": "This is generated through the OpenClaw tool interface.",
        "emotion": 1.0,
        "output_format": "file"
    }
    
    result = tool.generate_speech(params)
    print(f"\nGeneration result: {json.dumps(result, indent=2)}")


def example_7_streaming_simulation():
    """Example 7: Simulating real-time streaming"""
    print("\n" + "="*60)
    print("Example 7: Streaming Simulation")
    print("="*60)
    
    tts = ChatterboxTTS(
        config=ChatterboxConfig(
            emotion_scale=0.8,
            # Smaller max_length for faster generation
            max_length=512
        )
    )
    
    # Simulate streaming by generating chunks
    chunks = [
        "First sentence here.",
        "Second sentence continues.",
        "Third sentence wraps up."
    ]
    
    for i, chunk in enumerate(chunks):
        print(f"\nGenerating chunk {i+1}: {chunk}")
        audio = tts.generate(chunk)
        tts.save_audio(audio, f"output/example7_chunk_{i+1}.wav")


if __name__ == "__main__":
    import json
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    print("="*60)
    print("Chatterbox TTS - Usage Examples")
    print("="*60)
    
    # Run examples (uncomment the ones you want to test)
    
    # Basic usage
    # example_1_basic_tts()
    
    # Emotion control
    # example_2_emotion_control()
    
    # Multilingual
    # example_3_multilingual()
    
    # Voice cloning (requires reference audio)
    # example_4_voice_cloning()
    
    # Batch processing
    # example_5_batch_generation()
    
    # OpenClaw integration
    # example_6_openclaw_integration()
    
    # Streaming
    # example_7_streaming_simulation()
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("Uncomment the examples you want to run in the script.")
    print("="*60)
