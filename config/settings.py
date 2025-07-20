"""
AI Assistant Configuration Settings
Central configuration for all modules and features
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Central configuration manager for the AI Assistant"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.models_dir = self.base_dir / "models"
        self.logs_dir = self.base_dir / "data" / "logs"
        
        # Create necessary directories
        self._create_directories()
        
        # Load configuration
        self.settings = self._load_config()
        
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.data_dir,
            self.models_dir,
            self.logs_dir,
            self.data_dir / "conversations",
            self.data_dir / "preferences",
            self.data_dir / "knowledge_base",
            self.models_dir / "whisper",
            self.models_dir / "tts",
            self.models_dir / "llm",
            self.models_dir / "embeddings"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        config_file = Path(self.config_path)
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default configuration
            default_config = self._get_default_config()
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration settings"""
        return {
            "assistant": {
                "name": "JARVIS",
                "wake_word": "hey jarvis",
                "language": "en",
                "personality": "professional",
                "debug_mode": False,
                "log_level": "INFO"
            },
            
            "voice": {
                "speech_recognition": {
                    "engine": "whisper",
                    "model_size": "base",
                    "language": "en",
                    "timeout": 5,
                    "energy_threshold": 4000,
                    "pause_threshold": 0.8
                },
                "text_to_speech": {
                    "engine": "pyttsx3",
                    "voice_id": "default",
                    "rate": 150,
                    "volume": 0.9,
                    "fallback_engine": "coqui"
                },
                "wake_word_detection": {
                    "enabled": True,
                    "sensitivity": 0.8,
                    "timeout": 3
                },
                "emotion_detection": {
                    "enabled": True,
                    "model": "emotion-english-distilroberta-base"
                }
            },
            
            "ai": {
                "llm": {
                    "model": "gpt4all",
                    "model_path": "models/llm/gpt4all-model.bin",
                    "max_tokens": 2048,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                "embeddings": {
                    "model": "all-MiniLM-L6-v2",
                    "dimension": 384
                },
                "vector_database": {
                    "type": "chromadb",
                    "persist_directory": "data/knowledge_base"
                },
                "memory": {
                    "max_conversations": 100,
                    "context_window": 10,
                    "forget_after_days": 30
                }
            },
            
            "modules": {
                "system_control": {
                    "enabled": True,
                    "require_confirmation": True,
                    "allowed_apps": ["notepad", "calculator", "chrome", "firefox"]
                },
                "code_assistant": {
                    "enabled": True,
                    "supported_languages": ["python", "javascript", "java", "cpp", "html", "css"],
                    "auto_format": True,
                    "suggest_improvements": True
                },
                "file_manager": {
                    "enabled": True,
                    "root_paths": ["."],
                    "max_file_size": 10000000  # 10MB
                },
                "web_integration": {
                    "enabled": True,
                    "search_engine": "duckduckgo",
                    "max_results": 5,
                    "cache_results": True
                },
                "smart_home": {
                    "enabled": False,
                    "devices": {},
                    "mqtt_broker": "localhost",
                    "mqtt_port": 1883
                },
                "calendar": {
                    "enabled": True,
                    "calendar_file": "data/calendar.ics",
                    "reminder_check_interval": 60
                },
                "security": {
                    "enabled": True,
                    "voice_authentication": False,
                    "face_recognition": False,
                    "encrypt_data": True,
                    "log_all_actions": True
                }
            },
            
            "ui": {
                "interface": "cli",  # cli, gui, web
                "theme": "dark",
                "show_confidence": True,
                "show_processing_time": True
            },
            
            "logging": {
                "level": "INFO",
                "file": "data/logs/assistant.log",
                "max_size": 10485760,  # 10MB
                "backup_count": 5,
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            
            "paths": {
                "data_dir": str(self.data_dir),
                "models_dir": str(self.models_dir),
                "logs_dir": str(self.logs_dir),
                "conversations_dir": str(self.data_dir / "conversations"),
                "preferences_dir": str(self.data_dir / "preferences"),
                "knowledge_base_dir": str(self.data_dir / "knowledge_base")
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.settings
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated configuration
        self._save_config(self.settings)
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        for key, value in updates.items():
            self.set(key, value)
    
    def reload(self):
        """Reload configuration from file"""
        self.settings = self._load_config()
    
    def export(self, filepath: str):
        """Export configuration to file"""
        with open(filepath, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def import_config(self, filepath: str):
        """Import configuration from file"""
        with open(filepath, 'r') as f:
            imported_config = json.load(f)
        
        # Merge with existing config
        self._merge_configs(self.settings, imported_config)
        self._save_config(self.settings)
    
    def _merge_configs(self, base: Dict, update: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

# Global configuration instance
config = Config()

# Convenience functions
def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value"""
    return config.get(key, default)

def set_config(key: str, value: Any):
    """Set configuration value"""
    config.set(key, value)

def update_config(updates: Dict[str, Any]):
    """Update multiple configuration values"""
    config.update(updates) 