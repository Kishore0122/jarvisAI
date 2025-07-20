"""
System Assistant Module
Provides file operations, system control, and personal assistant tasks
"""

import os
import sys
import subprocess
import platform
import logging
import glob
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import webbrowser
import psutil

logger = logging.getLogger(__name__)

class SystemAssistant:
    """System assistant for file operations and system control"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.home_dir = Path.home()
        self.current_dir = Path.cwd()
        
        # Common file extensions
        self.text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv'}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'}
        self.video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'}
        self.audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'}
        
        logger.info(f"System Assistant initialized for {self.system}")
    
    def open_file(self, file_path: str) -> Dict[str, Any]:
        """Open a file with appropriate application"""
        try:
            file_path = Path(file_path)
            
            # Resolve relative paths
            if not file_path.is_absolute():
                file_path = self.current_dir / file_path
            
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f"File not found: {file_path}",
                    'error': 'File does not exist'
                }
            
            # Open file based on extension
            if self.system == 'windows':
                os.startfile(str(file_path))
            elif self.system == 'darwin':  # macOS
                subprocess.run(['open', str(file_path)])
            else:  # Linux
                subprocess.run(['xdg-open', str(file_path)])
            
            return {
                'success': True,
                'message': f"Opened file: {file_path.name}",
                'file': str(file_path)
            }
            
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            return {
                'success': False,
                'message': f"Failed to open file: {file_path}",
                'error': str(e)
            }
    
    def search_files(self, query: str, directory: str = None, file_type: str = None) -> Dict[str, Any]:
        """Search for files in directory"""
        try:
            search_dir = Path(directory) if directory else self.home_dir
            
            if not search_dir.exists():
                return {
                    'success': False,
                    'message': f"Directory not found: {search_dir}",
                    'error': 'Directory does not exist'
                }
            
            # Build search pattern
            if file_type:
                pattern = f"*{file_type}"
            else:
                pattern = "*"
            
            # Search for files
            found_files = []
            for file_path in search_dir.rglob(pattern):
                if query.lower() in file_path.name.lower():
                    found_files.append({
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': file_path.stat().st_size,
                        'type': 'file' if file_path.is_file() else 'directory'
                    })
            
            return {
                'success': True,
                'message': f"Found {len(found_files)} files matching '{query}'",
                'files': found_files[:20],  # Limit to 20 results
                'total': len(found_files)
            }
            
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return {
                'success': False,
                'message': f"Failed to search files: {query}",
                'error': str(e)
            }
    
    def list_directory(self, directory: str = None) -> Dict[str, Any]:
        """List contents of a directory"""
        try:
            target_dir = Path(directory) if directory else self.current_dir
            
            if not target_dir.exists():
                return {
                    'success': False,
                    'message': f"Directory not found: {target_dir}",
                    'error': 'Directory does not exist'
                }
            
            items = []
            for item in target_dir.iterdir():
                try:
                    stat = item.stat()
                    items.append({
                        'name': item.name,
                        'type': 'directory' if item.is_dir() else 'file',
                        'size': stat.st_size,
                        'modified': stat.st_mtime
                    })
                except:
                    continue
            
            # Sort: directories first, then files
            items.sort(key=lambda x: (x['type'] == 'file', x['name'].lower()))
            
            return {
                'success': True,
                'message': f"Contents of {target_dir}",
                'items': items[:50],  # Limit to 50 items
                'directory': str(target_dir)
            }
            
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return {
                'success': False,
                'message': f"Failed to list directory: {directory}",
                'error': str(e)
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        try:
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory info
            memory = psutil.virtual_memory()
            
            # Disk info
            disk = psutil.disk_usage('/')
            
            # System info
            system_info = {
                'platform': platform.platform(),
                'system': platform.system(),
                'release': platform.release(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'cpu': {
                    'usage': f"{cpu_percent}%",
                    'cores': cpu_count
                },
                'memory': {
                    'total': f"{memory.total // (1024**3)} GB",
                    'available': f"{memory.available // (1024**3)} GB",
                    'used': f"{memory.percent}%"
                },
                'disk': {
                    'total': f"{disk.total // (1024**3)} GB",
                    'free': f"{disk.free // (1024**3)} GB",
                    'used': f"{disk.percent}%"
                }
            }
            
            return {
                'success': True,
                'message': 'System information retrieved',
                'info': system_info
            }
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {
                'success': False,
                'message': 'Failed to get system information',
                'error': str(e)
            }
    
    def open_application(self, app_name: str) -> Dict[str, Any]:
        """Try to open an application by name, then as a website, then as a Google search."""
        import subprocess
        import platform
        app_name_clean = app_name.strip().lower()
        try:
            # Try to open as a system application
            if platform.system().lower() == 'windows':
                try:
                    subprocess.Popen([app_name_clean])
                    return {
                        'success': True,
                        'message': f"Opened application: {app_name_clean}",
                        'app': app_name_clean
                    }
                except Exception:
                    pass
            elif platform.system().lower() == 'darwin':
                try:
                    subprocess.Popen(['open', '-a', app_name_clean])
                    return {
                        'success': True,
                        'message': f"Opened application: {app_name_clean}",
                        'app': app_name_clean
                    }
                except Exception:
                    pass
            else:  # Linux
                try:
                    subprocess.Popen([app_name_clean])
                    return {
                        'success': True,
                        'message': f"Opened application: {app_name_clean}",
                        'app': app_name_clean
                    }
                except Exception:
                    pass
            # If app open fails, try as a website
            url = f"https://{app_name_clean}.com"
            try:
                webbrowser.open(url)
                return {
                    'success': True,
                    'message': f"Opened website: {url}",
                    'app': app_name_clean
                }
            except Exception:
                pass
            # If website open fails, try Google search
            search_url = f"https://www.google.com/search?q={app_name_clean}"
            webbrowser.open(search_url)
            return {
                'success': True,
                'message': f"Opened Google search for: {app_name_clean}",
                'app': app_name_clean
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open {app_name_clean}",
                'error': str(e)
            }
    
    def open_website(self, url: str) -> Dict[str, Any]:
        """Open a website in default browser"""
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            
            return {
                'success': True,
                'message': f"Opened website: {url}",
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error opening website: {e}")
            return {
                'success': False,
                'message': f"Failed to open website: {url}",
                'error': str(e)
            }
    
    def create_file(self, file_path: str, content: str = "") -> Dict[str, Any]:
        """Create a new file"""
        try:
            file_path = Path(file_path)
            
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create file with content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'success': True,
                'message': f"Created file: {file_path.name}",
                'file': str(file_path)
            }
            
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return {
                'success': False,
                'message': f"Failed to create file: {file_path}",
                'error': str(e)
            }
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete a file or directory"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f"File not found: {file_path}",
                    'error': 'File does not exist'
                }
            
            if file_path.is_file():
                file_path.unlink()
                action = "deleted"
            else:
                shutil.rmtree(file_path)
                action = "removed"
            
            return {
                'success': True,
                'message': f"{action.capitalize()} {file_path.name}",
                'file': str(file_path)
            }
            
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return {
                'success': False,
                'message': f"Failed to delete {file_path}",
                'error': str(e)
            }
    
    def get_current_directory(self) -> str:
        """Get current working directory"""
        return str(self.current_dir)
    
    def change_directory(self, directory: str) -> Dict[str, Any]:
        """Change current working directory"""
        try:
            new_dir = Path(directory)
            
            if not new_dir.exists():
                return {
                    'success': False,
                    'message': f"Directory not found: {directory}",
                    'error': 'Directory does not exist'
                }
            
            if not new_dir.is_dir():
                return {
                    'success': False,
                    'message': f"Not a directory: {directory}",
                    'error': 'Path is not a directory'
                }
            
            os.chdir(new_dir)
            self.current_dir = new_dir
            
            return {
                'success': True,
                'message': f"Changed to directory: {new_dir}",
                'directory': str(new_dir)
            }
            
        except Exception as e:
            logger.error(f"Error changing directory: {e}")
            return {
                'success': False,
                'message': f"Failed to change directory: {directory}",
                'error': str(e)
            } 