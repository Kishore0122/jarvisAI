# 🤖 JARVIS - AI Assistant with Mistral 7B

A powerful, local AI assistant powered by Mistral 7B LLM with voice recognition, text-to-speech, system control, and code generation capabilities.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## ✨ Features

### 🧠 **AI Intelligence**
- **Mistral 7B LLM**: Local, offline AI processing
- **Conversational AI**: Natural language understanding
- **Context Awareness**: Maintains conversation history
- **Mathematical Calculations**: Evaluate complex expressions

### 🎤 **Voice Features**
- **Text-to-Speech**: Natural voice responses
- **Voice Recognition**: Offline speech-to-text (Vosk)
- **Hotword Detection**: "Jarvis" wake word
- **Voice Commands**: Full voice control

### 💻 **System Control**
- **File Operations**: Open, search, create, delete files
- **Application Launch**: Dynamic app opening
- **Website Access**: Smart web navigation
- **System Information**: CPU, memory, disk usage
- **Directory Navigation**: Change and list directories

### 👨‍💻 **Code Generation**
- **10+ Languages**: Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift
- **Code Templates**: Boilerplate generation
- **Editor Integration**: Open in VS Code, Sublime, etc.
- **Smart Suggestions**: Context-aware code generation

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (recommended)
- **Windows 10/11**
- **8GB+ RAM** (for optimal performance)
- **4GB+ free disk space**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai.git
   cd jarvis-ai
   ```

2. **Install Python 3.10** (if not installed)
   ```bash
   # Download from python.org or use winget
   winget install Python.Python.3.10
   ```

3. **Install dependencies**
   ```bash
   # Set Python 3.10 alias
   Set-Alias -Name python310 -Value "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
   
   # Install packages
   python310 -m pip install -r requirements.txt
   ```

4. **Download AI Model**
   ```bash
   python310 download_mistral_model.py
   ```

5. **Run JARVIS**
   ```bash
   python310 run.py
   ```

### Alternative Launch Methods

**Windows Batch File:**
```bash
start_jarvis.bat
```

**PowerShell Script:**
```bash
.\start_jarvis.ps1
```

## 🎯 Usage

### Basic Commands

| Command | Description |
|---------|-------------|
| `jarvis help` | Show all available commands |
| `jarvis 2+2+23*5*4%3^3` | Mathematical calculations |
| `jarvis open notepad` | Launch applications |
| `jarvis system info` | System information |
| `jarvis tts` | Toggle voice on/off |

### Voice Commands

**Text Hotword Mode:**
```
jarvis write a python calculator
jarvis open chrome
jarvis search for documents
```

**Voice Hotword Mode:**
```
Say "Jarvis" followed by your command
```

### File Operations

```bash
jarvis open file.txt              # Open a file
jarvis search for document        # Search files
jarvis list files                 # List directory contents
jarvis create newfile.txt         # Create a file
jarvis delete oldfile.txt         # Delete a file
jarvis cd Documents               # Change directory
```

### Code Generation

```bash
jarvis write a python calculator
jarvis create code hello.py
jarvis generate template javascript
jarvis edit file script.py
```

### System Control

```bash
jarvis open notepad              # Launch Notepad
jarvis open chrome               # Launch Chrome
jarvis open website google.com   # Open website
jarvis system info               # System status
jarvis pwd                       # Current directory
```

## 📁 Project Structure

```
jarvis-ai/
├── 🤖 core/                     # Main AI logic
│   ├── assistant.py             # Main assistant class
│   └── brain.py                 # LLM integration
├── 🔧 modules/                  # Feature modules
│   ├── llama_cpp_integration.py # Mistral 7B integration
│   ├── tts.py                   # Text-to-speech
│   ├── system_assistant.py      # System control
│   └── code_assistant.py        # Code generation
├── ⚙️ config/                   # Configuration files
├── 🧠 models/                   # AI models
│   ├── llm/                     # Language models
│   └── vosk-model/              # Voice recognition
├── 📄 README.md                 # This file
├── 📋 requirements.txt          # Python dependencies
├── 🚀 run.py                    # Main launcher
├── 📥 download_mistral_model.py # Model downloader
├── 🎯 start_jarvis.bat          # Windows launcher
├── 🎯 start_jarvis.ps1          # PowerShell launcher
└── 🚫 .gitignore                # Git exclusions
```

## 🔧 Configuration

### Model Settings
- **LLM**: Mistral 7B Instruct v0.1 (Q4_0 quantization)
- **Context Window**: 4096 tokens
- **Voice Model**: Vosk en-us-0.22
- **TTS Engine**: pyttsx3 (Windows)

### Performance Optimization
- **CPU**: Multi-threaded processing
- **Memory**: Efficient token management
- **Storage**: ~4GB model size
- **Response Time**: 2-5 seconds average

## 🛠️ Troubleshooting

### Common Issues

**1. Model Not Found**
```bash
# Download the model
python310 download_mistral_model.py
```

**2. Python 3.10 Not Found**
```bash
# Install Python 3.10
winget install Python.Python.3.10
```

**3. Voice Recognition Issues**
```bash
# Check microphone permissions
# Ensure Vosk model is downloaded
```

**4. Slow Performance**
```bash
# Close other applications
# Ensure 8GB+ RAM available
# Check CPU usage
```

### Error Messages

| Error | Solution |
|-------|----------|
| `Model file missing` | Run `python310 download_mistral_model.py` |
| `llama-cpp-python not installed` | Run `python310 -m pip install llama-cpp-python` |
| `No TTS engines available` | Run `python310 -m pip install pyttsx3` |
| `Vosk model not found` | Model downloads automatically |

## 📊 System Requirements

### Minimum
- **OS**: Windows 10/11
- **Python**: 3.10+
- **RAM**: 8GB
- **Storage**: 4GB free space
- **CPU**: Multi-core processor

### Recommended
- **OS**: Windows 11
- **Python**: 3.10.11
- **RAM**: 16GB+
- **Storage**: 8GB free space
- **CPU**: Intel i5/AMD Ryzen 5 or better

## 🔒 Privacy & Security

- **100% Local**: No data sent to external servers
- **Offline Processing**: All AI processing on your device
- **No API Keys**: No external dependencies
- **Open Source**: Transparent codebase

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mistral AI** for the 7B language model
- **TheBloke** for GGUF quantization
- **Vosk** for offline speech recognition
- **LLaMA.cpp** for efficient model inference

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/jarvis-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jarvis-ai/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/jarvis-ai/wiki)

---

**Made with ❤️ for the AI community**

*JARVIS - Your Personal AI Assistant* 