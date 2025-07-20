"""
Code Assistant Module
Provides code generation, file creation, and editor integration
"""

import os
import sys
import logging
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CodeAssistant:
    """Code assistant for programming tasks and file creation"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.supported_languages = {
            'python': {
                'extensions': ['.py'],
                'comment': '#',
                'editors': ['vscode', 'pycharm', 'sublime', 'notepad++'],
                'template': '#!/usr/bin/env python3\n"""\n{description}\n"""\n\n{code}'
            },
            'javascript': {
                'extensions': ['.js', '.jsx'],
                'comment': '//',
                'editors': ['vscode', 'webstorm', 'sublime', 'notepad++'],
                'template': '// {description}\n\n{code}'
            },
            'java': {
                'extensions': ['.java'],
                'comment': '//',
                'editors': ['intellij', 'eclipse', 'vscode', 'notepad++'],
                'template': '// {description}\n\n{code}'
            },
            'cpp': {
                'extensions': ['.cpp', '.cc', '.cxx'],
                'comment': '//',
                'editors': ['vscode', 'clion', 'dev-c++', 'notepad++'],
                'template': '// {description}\n\n{code}'
            },
            'c': {
                'extensions': ['.c'],
                'comment': '//',
                'editors': ['vscode', 'dev-c++', 'codeblocks', 'notepad++'],
                'template': '// {description}\n\n{code}'
            },
            'html': {
                'extensions': ['.html', '.htm'],
                'comment': '<!--',
                'editors': ['vscode', 'sublime', 'notepad++', 'brackets'],
                'template': '<!-- {description} -->\n\n{code}'
            },
            'css': {
                'extensions': ['.css'],
                'comment': '/*',
                'editors': ['vscode', 'sublime', 'notepad++', 'brackets'],
                'template': '/* {description} */\n\n{code}'
            },
            'php': {
                'extensions': ['.php'],
                'comment': '//',
                'editors': ['vscode', 'phpstorm', 'sublime', 'notepad++'],
                'template': '<?php\n// {description}\n\n{code}\n?>'
            },
            'sql': {
                'extensions': ['.sql'],
                'comment': '--',
                'editors': ['vscode', 'mysql-workbench', 'pgadmin', 'notepad++'],
                'template': '-- {description}\n\n{code}'
            },
            'bash': {
                'extensions': ['.sh', '.bash'],
                'comment': '#',
                'editors': ['vscode', 'sublime', 'notepad++', 'vim'],
                'template': '#!/bin/bash\n# {description}\n\n{code}'
            }
        }
        
        # Common code editors and their commands
        self.editor_commands = {
            'vscode': 'code',
            'sublime': 'subl',
            'notepad++': 'notepad++',
            'vim': 'vim',
            'nano': 'nano',
            'pycharm': 'pycharm',
            'intellij': 'idea',
            'eclipse': 'eclipse',
            'dev-c++': 'devcpp',
            'codeblocks': 'codeblocks'
        }
        
        logger.info(f"Code Assistant initialized for {self.system}")
    
    def create_code_file(self, filename: str, language: str, code: str, description: str = "") -> Dict[str, Any]:
        """Create a code file with proper syntax and formatting"""
        try:
            # Determine language from filename or specified language
            detected_lang = self._detect_language(filename, language)
            
            if detected_lang not in self.supported_languages:
                return {
                    'success': False,
                    'message': f"Unsupported language: {detected_lang}",
                    'error': 'Language not supported'
                }
            
            # Get language configuration
            lang_config = self.supported_languages[detected_lang]
            
            # Ensure proper file extension
            if not any(filename.endswith(ext) for ext in lang_config['extensions']):
                filename = filename + lang_config['extensions'][0]
            
            # Create file path
            file_path = Path(filename)
            
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Format code with template
            formatted_code = lang_config['template'].format(
                description=description or f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                code=code
            )
            
            # Write code to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_code)
            
            return {
                'success': True,
                'message': f"Created {detected_lang} file: {file_path.name}",
                'file': str(file_path),
                'language': detected_lang,
                'size': len(formatted_code)
            }
            
        except Exception as e:
            logger.error(f"Error creating code file: {e}")
            return {
                'success': False,
                'message': f"Failed to create code file: {filename}",
                'error': str(e)
            }
    
    def open_in_editor(self, file_path: str, editor: str = None) -> Dict[str, Any]:
        """Open a file in a specific code editor"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f"File not found: {file_path}",
                    'error': 'File does not exist'
                }
            
            # Auto-detect editor if not specified
            if not editor:
                editor = self._detect_best_editor(file_path)
            
            # Get editor command
            if editor in self.editor_commands:
                editor_cmd = self.editor_commands[editor]
            else:
                # Try to use the editor name directly
                editor_cmd = editor
            
            # Open file in editor
            if self.system == 'windows':
                subprocess.Popen([editor_cmd, str(file_path)])
            else:
                subprocess.Popen([editor_cmd, str(file_path)])
            
            return {
                'success': True,
                'message': f"Opened {file_path.name} in {editor}",
                'file': str(file_path),
                'editor': editor
            }
            
        except Exception as e:
            logger.error(f"Error opening in editor: {e}")
            return {
                'success': False,
                'message': f"Failed to open {file_path} in {editor}",
                'error': str(e)
            }
    
    def generate_code_template(self, language: str, template_type: str = "basic") -> str:
        """Generate code templates for different languages"""
        templates = {
            'python': {
                'basic': '''def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()''',
                'class': '''class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print(f"Hello, {self.name}!")

# Usage
obj = MyClass("World")
obj.greet()''',
                'function': '''def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Example usage
result = calculate_fibonacci(10)
print(f"Fibonacci(10) = {result}")'''
            },
            'javascript': {
                'basic': '''console.log("Hello, World!");''',
                'function': '''function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("World"));''',
                'class': '''class Person {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        console.log(`Hello, ${this.name}!`);
    }
}

const person = new Person("World");
person.greet();'''
            },
            'html': {
                'basic': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>Welcome to my website.</p>
</body>
</html>''',
                'form': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
</head>
<body>
    <h1>Contact Form</h1>
    <form>
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        
        <label for="message">Message:</label>
        <textarea id="message" name="message" rows="4" required></textarea><br><br>
        
        <button type="submit">Send</button>
    </form>
</body>
</html>'''
            }
        }
        
        if language in templates and template_type in templates[language]:
            return templates[language][template_type]
        else:
            return f"// {language} code template\n// Add your code here"
    
    def _detect_language(self, filename: str, specified_lang: str = None) -> str:
        """Detect programming language from filename or specification"""
        if specified_lang:
            return specified_lang.lower()
        
        # Detect from file extension
        file_ext = Path(filename).suffix.lower()
        
        for lang, config in self.supported_languages.items():
            if file_ext in config['extensions']:
                return lang
        
        # Default to Python if no match
        return 'python'
    
    def _detect_best_editor(self, file_path: Path) -> str:
        """Detect the best editor for a file type"""
        file_ext = file_path.suffix.lower()
        
        # Language-specific editor preferences
        editor_preferences = {
            '.py': ['vscode', 'pycharm', 'sublime'],
            '.js': ['vscode', 'webstorm', 'sublime'],
            '.java': ['intellij', 'eclipse', 'vscode'],
            '.cpp': ['vscode', 'clion', 'dev-c++'],
            '.html': ['vscode', 'sublime', 'brackets'],
            '.css': ['vscode', 'sublime', 'brackets'],
            '.php': ['vscode', 'phpstorm', 'sublime'],
            '.sql': ['vscode', 'mysql-workbench', 'pgadmin'],
            '.sh': ['vscode', 'sublime', 'vim']
        }
        
        if file_ext in editor_preferences:
            for editor in editor_preferences[file_ext]:
                if self._is_editor_available(editor):
                    return editor
        
        # Fallback to common editors
        fallback_editors = ['vscode', 'sublime', 'notepad++']
        for editor in fallback_editors:
            if self._is_editor_available(editor):
                return editor
        
        return 'notepad'  # Default system editor
    
    def _is_editor_available(self, editor: str) -> bool:
        """Check if an editor is available on the system"""
        try:
            if editor in self.editor_commands:
                cmd = self.editor_commands[editor]
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, 
                                      timeout=5)
                return result.returncode == 0
        except:
            pass
        return False
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages"""
        return list(self.supported_languages.keys())
    
    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get information about a programming language"""
        if language in self.supported_languages:
            return self.supported_languages[language]
        return {}
    
    def format_code(self, code: str, language: str) -> str:
        """Format code with proper syntax"""
        if language in self.supported_languages:
            lang_config = self.supported_languages[language]
            return lang_config['template'].format(
                description=f"Formatted code - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                code=code
            )
        return code 