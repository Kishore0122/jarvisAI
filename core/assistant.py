"""
Simplified AI Assistant with TTS Support, System Control, and Code Writing
Focused on Mistral 7B LLM for true conversational AI
"""

import os
import sys
import json
import logging
import time
import re
import zipfile
import urllib.request
from typing import Dict, Any, Optional
from pathlib import Path
import difflib

# Import core components
from core.brain import Brain
from modules.tts import TTS
from modules.system_assistant import SystemAssistant
from modules.code_assistant import CodeAssistant

logger = logging.getLogger(__name__)

HOTWORD = "jarvis"

APP_ALIASES = [
    'notepad', 'calculator', 'calc', 'chrome', 'firefox', 'explorer', 'cmd', 'terminal', 'vscode', 'sublime', 'notepad++', 'word', 'excel', 'powerpoint', 'paint', 'photos', 'edge', 'browser'
]

PORCUPINE_ACCESS_KEY = "YOUR_PICOVOICE_ACCESS_KEY_HERE"  # <-- Paste your key from https://console.picovoice.ai/

def ensure_vosk_model(model_path="vosk-model-en-us-0.22"):
    if os.path.exists(model_path):
        return True
    print(f"Vosk model not found at '{model_path}'. Downloading and extracting...")
    url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
    zip_path = "vosk-model-en-us-0.22.zip"
    try:
        print("Downloading model (~1.8GB, may take a while)...")
        urllib.request.urlretrieve(url, zip_path)
        print("Unzipping model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        os.remove(zip_path)
        print("Model downloaded and extracted successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to download or unzip Vosk model: {e}")
        return False


def fuzzy_hotword_in_text(hotword, text):
    words = text.split()
    for word in words:
        if difflib.SequenceMatcher(None, word, hotword).ratio() > 0.8:
            return True, word
    return False, None


class Assistant:
    """Simplified AI Assistant with Mistral 7B LLM, TTS, System Control, and Code Writing"""
    
    def __init__(self, name: str = "JARVIS", enable_tts: bool = True):
        self.name = name
        self.brain = Brain()
        self.conversation_history = []
        self.enable_tts = enable_tts
        
        # Initialize TTS if enabled
        self.tts = None
        if self.enable_tts:
            self.tts = TTS()
        
        # Initialize system assistant
        self.system = SystemAssistant()
        
        # Initialize code assistant
        self.code = CodeAssistant()
        
        logger.info(f"{self.name} initialized with Mistral 7B LLM, TTS: {self.tts.is_available() if self.tts else False}, System Control, and Code Writing")
    
    def chat(self, user_input: str, speak_response: bool = True) -> str:
        """Process user input and generate response"""
        try:
            # Check for system commands first
            system_response = self._handle_system_commands(user_input)
            if system_response:
                if self.enable_tts and self.tts and speak_response:
                    self.speak(system_response)
                return system_response
            
            # Check for code commands
            code_response = self._handle_code_commands(user_input)
            if code_response:
                if self.enable_tts and self.tts and speak_response:
                    self.speak(code_response)
                return code_response
            
            # Add to conversation history
            self.conversation_history.append({
                'timestamp': time.time(),
                'user': user_input,
                'assistant': None
            })
            
            # Generate response using Mistral 7B
            response = self.brain.answer(user_input)
            
            # Update conversation history
            self.conversation_history[-1]['assistant'] = response
            
            # Speak response if TTS is enabled and requested
            if self.enable_tts and self.tts and speak_response:
                self.speak(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            error_msg = "I encountered an error. Please try again."
            if self.enable_tts and self.tts:
                self.speak(error_msg)
            return error_msg
    
    def _handle_code_commands(self, user_input: str) -> Optional[str]:
        """Handle code writing and programming commands"""
        input_lower = user_input.lower().strip()
        
        # Code file creation
        if re.match(r'create (?:code|program|script) (.+)', input_lower):
            match = re.search(r'create (?:code|program|script) (.+)', input_lower)
            filename = match.group(1).strip()
            
            # Generate code using Mistral 7B
            code_prompt = f"Write a complete, working {filename} program. Include proper imports, main function, and example usage."
            code_response = self.brain.answer(code_prompt)
            
            # Extract language from filename
            language = self.code._detect_language(filename)
            
            # Create code file
            result = self.code.create_code_file(filename, language, code_response, f"Generated by {self.name}")
            
            if result['success']:
                response = f"{result['message']}\n\nCode generated:\n{code_response[:200]}..."
                
                # Try to open in editor
                editor_result = self.code.open_in_editor(result['file'])
                if editor_result['success']:
                    response += f"\n\nOpened in {editor_result['editor']}"
                
                return response
            else:
                return f"Error: {result['message']}"
        
        # Write specific code
        elif re.match(r'write (?:code|program) (.+)', input_lower):
            match = re.search(r'write (?:code|program) (.+)', input_lower)
            description = match.group(1).strip()
            
            # Generate code using Mistral 7B
            code_prompt = f"Write a complete, working program for: {description}. Include proper imports, main function, and example usage."
            code_response = self.brain.answer(code_prompt)
            
            # Create a default filename
            filename = f"generated_{int(time.time())}.py"
            
            # Create code file
            result = self.code.create_code_file(filename, 'python', code_response, description)
            
            if result['success']:
                response = f"{result['message']}\n\nCode generated:\n{code_response[:200]}..."
                
                # Try to open in editor
                editor_result = self.code.open_in_editor(result['file'])
                if editor_result['success']:
                    response += f"\n\nOpened in {editor_result['editor']}"
                
                return response
            else:
                return f"Error: {result['message']}"
        
        # Open file in editor
        elif re.match(r'edit (?:file|code) (.+)', input_lower):
            match = re.search(r'edit (?:file|code) (.+)', input_lower)
            file_path = match.group(1).strip()
            
            result = self.code.open_in_editor(file_path)
            return f"{result['message']}"
        
        # Generate code template
        elif re.match(r'(?:generate|create) (?:template|boilerplate) (.+)', input_lower):
            match = re.search(r'(?:generate|create) (?:template|boilerplate) (.+)', input_lower)
            language = match.group(1).strip()
            
            if language in self.code.get_supported_languages():
                template = self.code.generate_code_template(language, 'basic')
                filename = f"template_{language}.{self.code.supported_languages[language]['extensions'][0]}"
                
                result = self.code.create_code_file(filename, language, template, f"{language.title()} template")
                
                if result['success']:
                    response = f"{result['message']}\n\nTemplate:\n{template}"
                    
                    # Try to open in editor
                    editor_result = self.code.open_in_editor(result['file'])
                    if editor_result['success']:
                        response += f"\n\nOpened in {editor_result['editor']}"
                    
                    return response
                else:
                    return f"Error: {result['message']}"
            else:
                return f"Unsupported language: {language}. Supported: {', '.join(self.code.get_supported_languages())}"
        
        # List supported languages
        elif re.match(r'(?:supported|available) (?:languages|programming)', input_lower):
            languages = self.code.get_supported_languages()
            response = f"Supported programming languages:\n"
            for lang in languages:
                info = self.code.get_language_info(lang)
                extensions = ', '.join(info['extensions'])
                response += f"- {lang.title()}: {extensions}\n"
            return response
        
        return None
    
    def _handle_system_commands(self, user_input: str) -> Optional[str]:
        """Handle system commands and file operations"""
        input_lower = user_input.lower().strip()
        
        # Explicit file open
        if re.match(r'open file (.+)', input_lower):
            match = re.search(r'open file (.+)', input_lower)
            file_path = match.group(1).strip()
            result = self.system.open_file(file_path)
            if result['success']:
                return f"Opened file/folder: {file_path}"
            else:
                return f"Error: {result['message']}"

        # For any 'open X' command, always try open_application first
        if re.match(r'open (.+)', input_lower):
            match = re.search(r'open (.+)', input_lower)
            target = match.group(1).strip()
            result = self.system.open_application(target)
            if result['success']:
                return result['message']
            else:
                return f"Error: {result['message']}"
        
        # File operations
        if re.match(r'open (?:file )?(.+)', input_lower):
            match = re.search(r'open (?:file )?(.+)', input_lower)
            file_path = match.group(1).strip()
            result = self.system.open_file(file_path)
            return f"{result['message']}"
        
        elif re.match(r'search (?:for )?(?:files? )?(.+)', input_lower):
            match = re.search(r'search (?:for )?(?:files? )?(.+)', input_lower)
            query = match.group(1).strip()
            result = self.system.search_files(query)
            if result['success']:
                files = result['files'][:5]  # Show first 5 results
                response = f"{result['message']}\n"
                for file in files:
                    response += f"- {file['name']} ({file['path']})\n"
                return response
            else:
                return f"Error: {result['message']}"
        
        elif re.match(r'list (?:files?|directory|folder)', input_lower):
            result = self.system.list_directory()
            if result['success']:
                response = f"{result['message']}\n"
                for item in result['items'][:10]:  # Show first 10 items
                    response += f"- {item['name']} ({item['type']})\n"
                return response
            else:
                return f"Error: {result['message']}"
        
        # System information
        elif re.match(r'(?:system|computer) (?:info|information|status)', input_lower):
            result = self.system.get_system_info()
            if result['success']:
                info = result['info']
                response = f"System Information:\n"
                response += f"- Platform: {info['platform']}\n"
                response += f"- CPU: {info['cpu']['usage']} usage, {info['cpu']['cores']} cores\n"
                response += f"- Memory: {info['memory']['used']} used ({info['memory']['available']} available)\n"
                response += f"- Disk: {info['disk']['used']} used ({info['disk']['free']} free)\n"
                return response
            else:
                return f"Error: {result['message']}"
        
        # File management
        elif re.match(r'create (?:file )?(.+)', input_lower):
            match = re.search(r'create (?:file )?(.+)', input_lower)
            file_path = match.group(1).strip()
            result = self.system.create_file(file_path)
            return f"{result['message']}"
        
        elif re.match(r'delete (?:file )?(.+)', input_lower):
            match = re.search(r'delete (?:file )?(.+)', input_lower)
            file_path = match.group(1).strip()
            result = self.system.delete_file(file_path)
            return f"{result['message']}"
        
        # Directory navigation
        elif re.match(r'cd (.+)', input_lower):
            match = re.search(r'cd (.+)', input_lower)
            directory = match.group(1).strip()
            result = self.system.change_directory(directory)
            return f"{result['message']}"
        
        elif re.match(r'pwd|current directory|where am i', input_lower):
            current_dir = self.system.get_current_directory()
            return f"Current directory: {current_dir}"
        
        # Mathematical expressions
        elif re.match(r'^[\d\+\-\*\/\(\)\.\^\%\s]+$', user_input.strip()):
            try:
                # Replace ^ with ** for Python exponentiation
                expression = user_input.strip().replace('^', '**')
                # Evaluate the expression safely
                result = eval(expression)
                return f"Result: {result}"
            except Exception as e:
                return f"Error evaluating expression: {str(e)}"
        
        # Help command
        elif re.match(r'help|commands|what can you do', input_lower):
            return self._get_help_text()
        
        return None
    
    def _get_help_text(self) -> str:
        """Get help text for available commands"""
        help_text = """
Available Commands:

📁 File Operations:
- "open file.txt" - Open a file
- "search for document" - Search for files
- "list files" - List directory contents
- "create file.txt" - Create a new file
- "delete file.txt" - Delete a file

💻 System Control:
- "system info" - Get system information
- "open app notepad" - Open an application
- "open website google.com" - Open a website

📂 Navigation:
- "cd folder_name" - Change directory
- "pwd" - Show current directory

💻 Code Writing:
- "create code hello.py" - Create a Python program
- "write code calculator" - Write a calculator program
- "edit file script.py" - Open file in code editor
- "generate template python" - Create Python template
- "supported languages" - Show supported languages

🧮 Math & Calculations:
- "2+2" or "5*3" - Calculate mathematical expressions
- "2^3" - Calculate exponents (2 to the power of 3)

🎤 Voice Control:
- "tts" - Toggle voice on/off
- "status" - Show system status

💬 General:
- "help" - Show this help
- "quit" - Exit assistant

You can also ask me general questions and I'll respond with voice and text!
"""
        return help_text
    
    def speak(self, text: str) -> bool:
        """Speak text using TTS"""
        if not self.enable_tts or not self.tts:
            return False
        
        try:
            return self.tts.speak(text)
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get assistant status"""
        return {
            'name': self.name,
            'brain_status': self.brain.get_status(),
            'tts_status': self.tts.get_status() if self.tts else {'available': False},
            'system_status': {'available': True, 'platform': self.system.system},
            'code_status': {'available': True, 'languages': len(self.code.get_supported_languages())},
            'conversation_count': len(self.conversation_history),
            'tts_enabled': self.enable_tts,
            'current_directory': self.system.get_current_directory()
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def is_ready(self) -> bool:
        """Check if assistant is ready"""
        return self.brain.is_available()
    
    def toggle_tts(self) -> bool:
        """Toggle TTS on/off"""
        self.enable_tts = not self.enable_tts
        logger.info(f"TTS {'enabled' if self.enable_tts else 'disabled'}")
        return self.enable_tts
    
    def set_tts_engine(self, engine: str) -> bool:
        """Set TTS engine"""
        if self.tts:
            return self.tts.set_engine(engine)
        return False

def run_voice_hotword(assistant, hotword=HOTWORD):
    import sounddevice as sd
    import queue
    import vosk
    import json

    model_path = "vosk-model-en-us-0.22"
    if not ensure_vosk_model(model_path):
        print(f"❌ Could not set up Vosk model at '{model_path}'.")
        return

    print(f"🎤 Vosk voice mode enabled. Say '{hotword}' (or something similar) followed by your command.")
    print("Press Ctrl+C to exit.")

    q = queue.Queue()
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                          channels=1, callback=callback):
        print("Listening...")
        try:
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get("text", "").lower()
                    if not text:
                        continue
                    print(f"You said: {text}")
                    found, matched_word = fuzzy_hotword_in_text(hotword, text)
                    if found:
                        # Remove hotword (or similar) and pass the rest as command
                        command = text.split(matched_word, 1)[-1].strip()
                        if not command:
                            print(f"Say '{hotword}' followed by your command.")
                            continue
                        print(f"Detected hotword! Command: {command}")
                        response = assistant.chat(command)
                        print(f"{assistant.name}: {response}\n")
        except KeyboardInterrupt:
            print("\nExiting Vosk voice mode.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant")
    parser.add_argument('--voice-hotword', action='store_true', help='Enable voice hotword detection (Porcupine)')
    parser.add_argument('--hotword', type=str, default=HOTWORD, help='Set the hotword (default: jarvis)')
    args = parser.parse_args()

    print("🤖 JARVIS - Mistral 7B AI Assistant with TTS, System Control & Code Writing")
    print("=" * 70)
    
    assistant = Assistant(enable_tts=True)
    status = assistant.get_status()
    print(f"Model: {status['brain_status']['model']}")
    print(f"Available: {status['brain_status']['available']}")
    print(f"TTS: {status['tts_status']['available']} ({status['tts_status']['current_engine']})")
    print(f"System Control: {status['system_status']['available']} ({status['system_status']['platform']})")
    print(f"Code Writing: {status['code_status']['available']} ({status['code_status']['languages']} languages)")
    print(f"Current Directory: {status['current_directory']}")
    print()
    if not assistant.is_ready():
        print("❌ Mistral 7B model not available!")
        print("💡 Please download the model using: python download_mistral_model.py")
        print()
        return
    print("✅ Ready! Type 'quit' to exit")
    print("💬 Commands: 'help' for commands, 'tts' to toggle voice, 'status' for info")
    print("-" * 70)

    if args.voice_hotword:
        run_voice_hotword(assistant, hotword=args.hotword)
        return

    # Text hotword mode
    print(f"(Text hotword mode enabled. Type '{args.hotword} <your command>' to activate.)")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if not user_input.lower().startswith(args.hotword):
                print(f"(Waiting for hotword '{args.hotword}')")
                continue
            command = user_input[len(args.hotword):].strip()
            if command.lower() in ['quit', 'exit', 'bye']:
                assistant.speak("Goodbye!")
                print(f"{assistant.name}: Goodbye!")
                break
            response = assistant.chat(command)
            print(f"{assistant.name}: {response}\n")
        except KeyboardInterrupt:
            assistant.speak("Goodbye!")
            print(f"\n{assistant.name}: Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"{assistant.name}: I encountered an error. Please try again.")

if __name__ == "__main__":
    main() 