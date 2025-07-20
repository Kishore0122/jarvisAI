"""
Text-to-Speech Module
Supports multiple TTS engines for voice output
"""

import logging
import os
import sys
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class TTS:
    """Text-to-Speech with multiple engine support"""
    
    def __init__(self):
        self.engine = None
        self.available_engines = []
        self.current_engine = None
        
        # Initialize available engines
        self._initialize_engines()
        
        logger.info(f"TTS initialized with engines: {self.available_engines}")
    
    def _initialize_engines(self):
        """Initialize available TTS engines"""
        # Try pyttsx3 first (offline, no internet required)
        if self._try_pyttsx3():
            self.available_engines.append('pyttsx3')
        
        # Try coqui-ai (better quality, requires internet for first download)
        if self._try_coqui():
            self.available_engines.append('coqui')
        
        # Set default engine
        if self.available_engines:
            self.current_engine = self.available_engines[0]
            logger.info(f"Using TTS engine: {self.current_engine}")
        else:
            logger.warning("No TTS engines available")
    
    def _try_pyttsx3(self) -> bool:
        """Try to initialize pyttsx3 engine"""
        try:
            import pyttsx3
            self.pyttsx3_engine = pyttsx3.init()
            
            # Configure pyttsx3
            self.pyttsx3_engine.setProperty('rate', 150)  # Speed
            self.pyttsx3_engine.setProperty('volume', 0.9)  # Volume
            
            # Get available voices
            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                # Try to set a good voice
                for voice in voices:
                    if 'en' in voice.id.lower() or 'english' in voice.name.lower():
                        self.pyttsx3_engine.setProperty('voice', voice.id)
                        break
            
            logger.info("✅ pyttsx3 TTS engine initialized")
            return True
            
        except Exception as e:
            logger.warning(f"pyttsx3 not available: {e}")
            return False
    
    def _try_coqui(self) -> bool:
        """Try to initialize coqui-ai engine"""
        try:
            from TTS.api import TTS
            
            # Try to use a fast model
            model_name = "tts_models/en/ljspeech/tacotron2-DDC"
            
            # Check if model is available
            available_models = TTS.list_models()
            if model_name in available_models:
                self.coqui_tts = TTS(model_name)
                logger.info("✅ coqui-ai TTS engine initialized")
                return True
            else:
                logger.warning("coqui-ai model not available")
                return False
                
        except Exception as e:
            logger.warning(f"coqui-ai not available: {e}")
            return False
    
    def speak(self, text: str, engine: Optional[str] = None) -> bool:
        """Convert text to speech"""
        try:
            if not self.available_engines:
                logger.warning("No TTS engines available")
                return False
            
            # Use specified engine or default
            engine_to_use = engine or self.current_engine
            
            if engine_to_use == 'pyttsx3':
                return self._speak_pyttsx3(text)
            elif engine_to_use == 'coqui':
                return self._speak_coqui(text)
            else:
                logger.warning(f"Unknown TTS engine: {engine_to_use}")
                return False
                
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return False
    
    def _speak_pyttsx3(self, text: str) -> bool:
        """Speak using pyttsx3"""
        try:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"pyttsx3 speak error: {e}")
            return False
    
    def _speak_coqui(self, text: str) -> bool:
        """Speak using coqui-ai"""
        try:
            # Generate speech
            output_path = "temp_speech.wav"
            self.coqui_tts.tts_to_file(text=text, file_path=output_path)
            
            # Play the audio
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Clean up
            pygame.mixer.quit()
            if os.path.exists(output_path):
                os.remove(output_path)
            
            return True
            
        except Exception as e:
            logger.error(f"coqui speak error: {e}")
            return False
    
    def get_available_engines(self) -> list:
        """Get list of available TTS engines"""
        return self.available_engines.copy()
    
    def set_engine(self, engine: str) -> bool:
        """Set the TTS engine to use"""
        if engine in self.available_engines:
            self.current_engine = engine
            logger.info(f"TTS engine set to: {engine}")
            return True
        else:
            logger.warning(f"TTS engine not available: {engine}")
            return False
    
    def is_available(self) -> bool:
        """Check if TTS is available"""
        return len(self.available_engines) > 0
    
    def get_status(self) -> Dict[str, Any]:
        """Get TTS status"""
        return {
            'available': self.is_available(),
            'current_engine': self.current_engine,
            'available_engines': self.get_available_engines()
        } 