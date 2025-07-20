#!/usr/bin/env python3
"""
Run JARVIS - Mistral 7B AI Assistant
Simple launcher script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.assistant import main

if __name__ == "__main__":
    main() 