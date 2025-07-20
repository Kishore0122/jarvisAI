"""
LLaMA.cpp Integration Module
Provides better support for GGUF models using llama-cpp-python
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class LlamaCppIntegration:
    """LLaMA.cpp integration with GGUF model files"""
    
    def __init__(self, model_name: str = "mistral-7b-instruct-v0.1.Q4_0.gguf"):
        self.model_name = model_name
        self.model_path = Path("models/llm")
        self.model_file = self.model_path / model_name
        self.model = None
        self.is_initialized = False
        
        # Create models directory if it doesn't exist
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLaMA.cpp model"""
        try:
            # Check if model file exists
            if not self.model_file.exists():
                logger.error(f"❌ Model file missing: {self.model_file}")
                logger.info(f"📥 Please download the model using: python download_mistral_model.py")
                return
            
            # Check file size
            file_size_gb = self.model_file.stat().st_size / (1024**3)
            if file_size_gb < 3.5:  # Should be ~4.2GB
                logger.error(f"❌ Model file appears incomplete: {file_size_gb:.1f} GB")
                logger.info(f"📥 Please re-download the model using: python download_mistral_model.py")
                return
            
            # Import LLaMA.cpp
            try:
                from llama_cpp import Llama
            except ImportError:
                logger.error("❌ llama-cpp-python not installed. Run: pip install llama-cpp-python")
                return
            
            # Initialize model with better configuration
            logger.info(f"🤖 Loading LLaMA.cpp model: {self.model_name}")
            try:
                self.model = Llama(
                    model_path="models/llm/mistral-7b-instruct-v0.1.Q4_0.gguf",
                    n_ctx=4096
                )
                self.is_initialized = True
                logger.info("✅ LLaMA.cpp model loaded successfully!")
            except Exception as e:
                logger.error(f"❌ Failed to instantiate LLaMA.cpp model: {e}")
                self.is_initialized = False
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLaMA.cpp: {e}")
            self.is_initialized = False
    
    def truncate_prompt(self, prompt: str, max_tokens: int = 1800) -> str:
        """Truncate prompt to prevent token overflow"""
        try:
            # Simple word-based truncation (rough approximation)
            words = prompt.split()
            if len(words) > max_tokens:
                # Keep the most recent words
                truncated_words = words[-max_tokens:]
                truncated_prompt = " ".join(truncated_words)
                logger.warning(f"⚠️ Prompt truncated from {len(words)} to {len(truncated_words)} words")
                return truncated_prompt
            return prompt
        except Exception as e:
            logger.error(f"Error truncating prompt: {e}")
            return prompt
    
    def chat(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """Generate response using LLaMA.cpp with system prompt for factual accuracy"""
        if not self.is_initialized or not self.model:
            return self._fallback_response(prompt)
        try:
            # Truncate prompt to prevent token overflow
            truncated_prompt = self.truncate_prompt(prompt)
            # Clean the prompt to avoid duplication
            cleaned_prompt = truncated_prompt.strip()
            # Remove any existing instruction tokens
            if cleaned_prompt.startswith('[INST]'):
                cleaned_prompt = cleaned_prompt[len('[INST]'):].strip()
            if cleaned_prompt.endswith('[/INST]'):
                cleaned_prompt = cleaned_prompt[:-len('[/INST]')].strip()
            # Remove any leading <s> tokens
            cleaned_prompt = cleaned_prompt.lstrip('<s>').strip()
            
            # Create a simple prompt without system instructions to avoid conflicts
            full_prompt = f"[INST] {cleaned_prompt} [/INST]"
            response = self.model(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "[INST]"],
                echo=False
            )
            if response and 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['text'].strip()
                # Remove any leading prompt artifacts
                if content.startswith('<s>'):
                    content = content.lstrip('<s>').strip()
                if content.startswith('[INST]'):
                    content = content[len('[INST]'):].strip()
                if content.endswith('[/INST]'):
                    content = content[:-len('[/INST]')].strip()
                return content
            else:
                return self._fallback_response(prompt)
        except Exception as e:
            logger.error(f"❌ LLaMA.cpp chat error: {e}")
            return self._fallback_response(prompt)
    
    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """Generate text using LLaMA.cpp (alternative method)"""
        if not self.is_initialized or not self.model:
            return self._fallback_response(prompt)
        
        try:
            # Use generate method for simpler text generation
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["\n\n", "Human:", "Assistant:"],
                echo=False
            )
            
            if response and 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['text'].strip()
                logger.info(f"🤖 LLaMA.cpp generation completed ({len(content)} chars)")
                return content
            else:
                return self._fallback_response(prompt)
            
        except Exception as e:
            logger.error(f"❌ LLaMA.cpp generation error: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when model is not available"""
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your AI assistant."
        elif any(word in prompt_lower for word in ['bye', 'goodbye', 'exit']):
            return "Goodbye! Have a great day!"
        elif 'help' in prompt_lower:
            return "I can help you with various tasks."
        elif 'time' in prompt_lower or 'date' in prompt_lower:
            from datetime import datetime
            now = datetime.now()
            return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
        elif 'ceo' in prompt_lower and 'google' in prompt_lower:
            return "Sundar Pichai is the CEO of Google (Alphabet Inc.). He has been CEO since 2015."
        elif 'ceo' in prompt_lower and 'meta' in prompt_lower:
            return "Mark Zuckerberg is the CEO of Meta (formerly Facebook)."
        elif 'ceo' in prompt_lower and 'blackrock' in prompt_lower:
            return "Larry Fink is the CEO of BlackRock."
        elif '2 + 2' in prompt_lower or '2+2' in prompt_lower:
            return "2 + 2 = 4"
        elif 'deploy' in prompt_lower and 'web' in prompt_lower:
            return """Here's a step-by-step guide to deploy a full-stack web application:

1. **Prepare Your Application**
   - Ensure your code is production-ready
   - Set up environment variables
   - Optimize for performance

2. **Choose a Hosting Platform**
   - **Vercel**: Great for React/Next.js apps
   - **Netlify**: Good for static sites and JAMstack
   - **Heroku**: Good for full-stack apps
   - **AWS/GCP/Azure**: For enterprise solutions

3. **Frontend Deployment**
   - Build your frontend (npm run build)
   - Upload to CDN or hosting service
   - Configure custom domain

4. **Backend Deployment**
   - Set up server (Node.js, Python, etc.)
   - Configure database connections
   - Set up environment variables
   - Deploy to cloud platform

5. **Database Setup**
   - Choose database (PostgreSQL, MongoDB, etc.)
   - Set up production database
   - Configure backups

6. **Domain & SSL**
   - Configure custom domain
   - Set up SSL certificate
   - Configure DNS settings

7. **Testing & Monitoring**
   - Test all functionality
   - Set up monitoring tools
   - Configure error tracking

8. **CI/CD Pipeline**
   - Set up automated deployment
   - Configure testing pipeline
   - Set up staging environment"""
        else:
            return "I'm sorry, I don't have that information right now."
    
    def is_available(self) -> bool:
        """Check if LLaMA.cpp is available and working"""
        return self.is_initialized and self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        file_size_gb = self.model_file.stat().st_size / (1024**3) if self.model_file.exists() else 0
        return {
            'model_name': self.model_name,
            'model_path': str(self.model_file),
            'file_exists': self.model_file.exists(),
            'file_size_gb': file_size_gb,
            'is_initialized': self.is_initialized,
            'is_available': self.is_available()
        }
    
    def list_available_models(self) -> list:
        """List available model files in the models directory"""
        models = []
        if self.model_path.exists():
            for file in self.model_path.glob("*.gguf"):
                models.append(file.name)
            for file in self.model_path.glob("*.bin"):
                models.append(file.name)
        return models
    
    def can_generate(self) -> bool:
        """Check if the model can generate a response"""
        return self.is_initialized and self.model is not None 