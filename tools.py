import re
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class TextProcessor:
    """Utility class for text processing operations"""
    
    @staticmethod
    def clean_dialogue(text: str) -> str:
        """Remove stage directions and actions between brackets/parentheses"""
        if not text:
            return ""
            
        # Remove content in parentheses like (smiling), (laughing), etc.
        cleaned = re.sub(r"\([^)]*\)", "", text)
        # Remove content in square brackets like [nodding], [gesturing], etc.
        cleaned = re.sub(r"\[[^\]]*\]", "", cleaned)
        # Remove content in curly braces like {action}, etc.
        cleaned = re.sub(r"\{[^}]*\}", "", cleaned)
        
        # Clean up extra whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)
        # Clean up multiple newlines but preserve paragraph structure
        cleaned = re.sub(r"\n\s*\n\s*\n+", "\n\n", cleaned)
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in cleaned.split('\n')]
        cleaned = '\n'.join(line for line in lines if line)
        
        return cleaned.strip()
    
    @staticmethod
    def extract_score(score_text: str) -> str:
        """Extract numerical score from scoring agent output"""
        if not score_text:
            return "0"
            
        lines = score_text.strip().split("\n")
        if not lines:
            return "0"
            
        # Get the first line and extract any numbers
        first_line = lines[0].strip()
        
        # Look for standalone number first
        standalone_match = re.match(r"^(\d+)$", first_line)
        if standalone_match:
            score = int(standalone_match.group(1))
            return str(min(max(score, 1), 10))  # Ensure score is between 1-10
        
        # Look for a number with /10 or other formats
        fraction_match = re.search(r"(\d+)(?:/10|/\d+)", first_line)
        if fraction_match:
            score = int(fraction_match.group(1))
            return str(min(max(score, 1), 10))
        
        # Look for any number in the first line
        number_match = re.search(r"(\d+)", first_line)
        if number_match:
            score = int(number_match.group(1))
            return str(min(max(score, 1), 10))
        
        return "0"
    
    @staticmethod
    def validate_discussion_content(content: str) -> bool:
        """Validate that discussion content is not empty and has minimum length"""
        if not content or not content.strip():
            return False
        
        # Check minimum length (increased for meaningful discussions)
        if len(content.strip()) < 100:
            return False
        
        # Check if it looks like actual discussion content
        # Should have some dialogue markers or multiple sentences
        lines = content.strip().split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        if len(non_empty_lines) < 3:  # At least 3 meaningful lines
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip('. ')
        # Ensure filename is not empty
        if not sanitized:
            sanitized = "output"
        return sanitized

class FileManager:
    """Utility class for file operations"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.output_dir = self.base_dir / "output"
        self.logs_dir = self.base_dir / "logs"
    
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        try:
            self.output_dir.mkdir(exist_ok=True)
            self.logs_dir.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directories: {e}")
    
    def save_result(self, content: str, filename: str) -> bool:
        """Save content to output directory with error handling"""
        if not content:
            print(f"Warning: Attempting to save empty content to {filename}")
            return False
        
        self.ensure_directories()
        
        # Sanitize filename
        safe_filename = TextProcessor.sanitize_filename(filename)
        output_path = self.output_dir / safe_filename
        
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"✅ Result saved to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving file {safe_filename}: {e}")
            return False
    
    def load_discussion_from_file(self, filename: str) -> str:
        """Load discussion content from file with improved error handling"""
        file_path = self.base_dir / filename
        
        try:
            if not file_path.exists():
                print(f"❌ Discussion file not found: {file_path}")
                return ""
            
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                
            if not content.strip():
                print(f"⚠️  Discussion file is empty: {file_path}")
                return ""
                
            print(f"✅ Loaded discussion from: {file_path}")
            return content
            
        except UnicodeDecodeError:
            try:
                # Try different encoding
                with open(file_path, "r", encoding="latin-1") as file:
                    content = file.read()
                print(f"✅ Loaded discussion with latin-1 encoding: {file_path}")
                return content
            except Exception as e:
                print(f"❌ Error loading discussion file with alternative encoding: {e}")
                return ""
        except Exception as e:
            print(f"❌ Error loading discussion file: {e}")
            return ""
    
    def save_log(self, log_content: str, log_name: str = None) -> bool:
        """Save log content with timestamp"""
        self.ensure_directories()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{log_name or 'process_log'}_{timestamp}.txt"
        log_path = self.logs_dir / log_filename
        
        try:
            with open(log_path, "w", encoding="utf-8") as file:
                file.write(f"Process Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 60 + "\n\n")
                file.write(log_content)
            print(f"📝 Log saved to: {log_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving log: {e}")
            return False

class ValidationTools:
    """Tools for validating inputs and outputs"""
    
    @staticmethod
    def validate_environment() -> bool:
        """Check if required environment variables are set"""
        required_vars = ["GOOGLE_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print("💡 Please set these variables in your .env file or environment:")
            for var in missing_vars:
                print(f"   {var}=your_api_key_here")
            return False
        
        # Validate API key format (basic check)
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and len(api_key.strip()) < 10:
            print("⚠️  Warning: GOOGLE_API_KEY seems too short. Please verify it's correct.")
        
        print("✅ Environment validation passed")
        return True
    
    @staticmethod
    def validate_agent_response(response: str, agent_name: str) -> bool:
        """Validate that agent response is not empty and meaningful"""
        if not response or not response.strip():
            print(f"❌ Warning: {agent_name} returned empty response")
            return False
        
        if len(response.strip()) < 10:
            print(f"⚠️  Warning: {agent_name} returned very short response: '{response.strip()}'")
            return False
        
        print(f"✅ {agent_name} response validation passed")
        return True
    
    @staticmethod
    def validate_crew_result(result: Any) -> bool:
        """Validate crew execution result"""
        if result is None:
            print("❌ Crew returned None result")
            return False
        
        result_str = str(result).strip()
        if not result_str:
            print("❌ Crew returned empty result")
            return False
        
        if len(result_str) < 50:
            print(f"⚠️  Warning: Crew returned very short result: '{result_str[:100]}...'")
        
        return True

class LoggingTools:
    """Enhanced logging utilities"""
    
    _log_buffer = []
    
    @staticmethod
    def log_step(step_name: str, message: str = ""):
        """Log a processing step"""
        separator = "=" * 60
        log_entry = f"\n{separator}\nSTEP: {step_name}\n"
        if message:
            log_entry += f"INFO: {message}\n"
        log_entry += separator
        
        print(log_entry)
        LoggingTools._log_buffer.append(log_entry)
    
    @staticmethod
    def log_result(title: str, content: str, max_preview: int = 200):
        """Log results with preview"""
        log_entry = f"\n--- {title} ---\n"
        
        if content:
            preview = content[:max_preview] + "..." if len(content) > max_preview else content
            log_entry += f"{preview}\n"
        else:
            log_entry += "No content\n"
        
        log_entry += f"--- End {title} ---\n"
        
        print(log_entry)
        LoggingTools._log_buffer.append(log_entry)
    
    @staticmethod
    def log_error(error_msg: str, context: str = ""):
        """Log error messages"""
        log_entry = f"\n❌ ERROR"
        if context:
            log_entry += f" in {context}"
        log_entry += f": {error_msg}\n"
        
        print(log_entry)
        LoggingTools._log_buffer.append(log_entry)
    
    @staticmethod
    def get_full_log() -> str:
        """Get complete log as string"""
        return "\n".join(LoggingTools._log_buffer)
    
    @staticmethod
    def clear_log():
        """Clear the log buffer"""
        LoggingTools._log_buffer.clear()
    
    @staticmethod
    def save_log_to_file(file_manager: FileManager) -> bool:
        """Save complete log to file"""
        if LoggingTools._log_buffer:
            full_log = LoggingTools.get_full_log()
            return file_manager.save_log(full_log, "newsgroup_processing")
        return False