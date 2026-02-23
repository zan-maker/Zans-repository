#!/usr/bin/env python3
"""
OpenClaw Tool Integration for Chatterbox TTS
Enables voice generation via OpenClaw sessions
"""

import os
import sys
import json
import base64
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from chatterbox_tts import ChatterboxTTS, ChatterboxConfig


class OpenClawChatterboxTool:
    """
    OpenClaw-compatible tool wrapper for Chatterbox TTS
    
    This class provides a standardized interface for OpenClaw
    to call Chatterbox TTS functionality.
    """
    
    def __init__(self):
        self.tts = None
        self._initialized = False
    
    def initialize(self, config_dict: dict = None):
        """Initialize the TTS engine"""
        if config_dict:
            config = ChatterboxConfig(**config_dict)
        else:
            config = ChatterboxConfig()
        
        self.tts = ChatterboxTTS(config)
        self._initialized = True
        return {"status": "initialized", "device": config.device}
    
    def generate_speech(self, params: dict) -> dict:
        """
        Generate speech from text
        
        Parameters:
            text: str - Text to synthesize
            emotion: float (optional) - 0.0 to 2.0
            language: str (optional) - e.g., "en", "es"
            voice: str (optional) - Cloned voice name
            output_format: str (optional) - "wav", "mp3", "base64"
            
        Returns:
            Dictionary with audio data or file path
        """
        if not self._initialized:
            self.initialize()
        
        text = params.get("text", "")
        if not text:
            return {"error": "No text provided"}
        
        emotion = params.get("emotion", 1.0)
        language = params.get("language", "en")
        voice = params.get("voice")
        output_format = params.get("output_format", "base64")
        
        try:
            # Generate audio
            if voice:
                audio = self.tts.generate_with_cloned_voice(
                    text, voice, emotion_scale=emotion, language=language
                )
            else:
                audio = self.tts.generate(
                    text, emotion_scale=emotion, language=language
                )
            
            # Save temporarily
            temp_path = "/tmp/chatterbox_output.wav"
            self.tts.save_audio(audio, temp_path)
            
            # Return based on format
            if output_format == "base64":
                with open(temp_path, "rb") as f:
                    audio_b64 = base64.b64encode(f.read()).decode()
                return {
                    "success": True,
                    "audio_base64": audio_b64,
                    "format": "wav",
                    "sample_rate": 24000,
                    "text": text
                }
            else:
                return {
                    "success": True,
                    "file_path": temp_path,
                    "format": output_format,
                    "text": text
                }
                
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def clone_voice(self, params: dict) -> dict:
        """
        Clone a voice from reference audio
        
        Parameters:
            audio_path: str - Path to reference audio (5+ seconds)
            voice_name: str - Name to save voice under
            transcript: str (optional) - Transcript of reference audio
            
        Returns:
            Dictionary with success status
        """
        if not self._initialized:
            self.initialize()
        
        audio_path = params.get("audio_path")
        voice_name = params.get("voice_name")
        transcript = params.get("transcript")
        
        if not audio_path or not voice_name:
            return {"error": "audio_path and voice_name required"}
        
        success = self.tts.clone_voice(audio_path, voice_name, transcript)
        
        return {
            "success": success,
            "voice_name": voice_name,
            "message": f"Voice '{voice_name}' {'cloned' if success else 'failed'}"
        }
    
    def list_voices(self, params: dict = None) -> dict:
        """List available cloned voices"""
        if not self._initialized:
            self.initialize()
        
        voices = self.tts.list_cloned_voices()
        presets = self.tts.get_emotion_presets()
        
        return {
            "cloned_voices": voices,
            "emotion_presets": presets,
            "languages": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko"]
        }
    
    def health_check(self) -> dict:
        """Check if service is healthy"""
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "model": "resemble/chatterbox-0.5b",
            "local_inference": self.tts.model is not None if self.tts else False
        }


# CLI interface for OpenClaw tool calls
def main():
    """CLI entry point for OpenClaw integration"""
    tool = OpenClawChatterboxTool()
    
    # Read command from stdin (OpenClaw tool calling convention)
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        # Parse parameters from JSON argument or stdin
        if len(sys.argv) > 2:
            params = json.loads(sys.argv[2])
        else:
            params = json.loads(sys.stdin.read())
        
        # Route to appropriate method
        if command == "initialize":
            result = tool.initialize(params)
        elif command == "generate":
            result = tool.generate_speech(params)
        elif command == "clone":
            result = tool.clone_voice(params)
        elif command == "list_voices":
            result = tool.list_voices(params)
        elif command == "health":
            result = tool.health_check()
        else:
            result = {"error": f"Unknown command: {command}"}
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
    else:
        # Interactive mode
        print("Chatterbox TTS Tool - OpenClaw Integration")
        print("Usage: python openclaw_tool.py <command> <params_json>")
        print("")
        print("Commands:")
        print("  initialize  - Initialize TTS engine")
        print("  generate    - Generate speech from text")
        print("  clone       - Clone a voice")
        print("  list_voices - List available voices")
        print("  health      - Check service health")


if __name__ == "__main__":
    main()
