"""
Simplified AI Brain Module
Focused on Mistral 7B LLM for true conversational AI
"""

import os
import sys
import json
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Import Mistral LLM integration
from modules.llama_cpp_integration import LlamaCppIntegration

logger = logging.getLogger(__name__)

class Brain:
    """Simplified AI brain with Mistral 7B LLM"""
    
    def __init__(self):
        self.llm = None
        self.is_initialized = False
        
        # Initialize Mistral 7B
        self._initialize_mistral()
        
        logger.info("Brain initialized with Mistral 7B LLM")
    
    def _initialize_mistral(self):
        """Initialize Mistral 7B LLM"""
        try:
            self.llm = LlamaCppIntegration()
            if self.llm.is_initialized:
                self.is_initialized = True
                logger.info("✅ Mistral 7B LLM initialized successfully")
            else:
                logger.warning("❌ Mistral 7B LLM not available - please download the model")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Mistral 7B: {e}")
    
    def answer(self, user_input: str) -> str:
        """Generate response using Mistral 7B LLM"""
        try:
            if not self.is_initialized or not self.llm:
                return "I'm sorry, but my AI model is not available. Please download the Mistral model using: python download_mistral_model.py"
            
            # Generate response using Mistral 7B
            response = self.llm.chat(user_input)
            
            if response and response.strip():
                return response.strip()
            else:
                return "I'm sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error while processing your request. Please try again."
    
    def is_available(self) -> bool:
        """Check if Mistral 7B is available"""
        return self.is_initialized and self.llm is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current brain status"""
        return {
            'model': 'mistral-7b-instruct-v0.1.Q4_0.gguf',
            'available': self.is_available(),
            'initialized': self.is_initialized
        } 