"""
Centralized configuration loader for the email workflow.
Loads settings from workflow_config.yaml and environment variables from .env file.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigLoader:
    """Loads and manages configuration from YAML and .env files."""

    def __init__(self, config_path: str = "workflow_config.yaml"):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_env()
        self._load_yaml()

    def _load_env(self):
        """Load environment variables from .env file."""
        env_path = Path(".env")
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            print(f"✅ Loaded environment variables from {env_path}")
        else:
            # Try to load from environment anyway
            load_dotenv()
            # Check if we have required API keys
            if not os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
                print(f"⚠️  No .env file found. Create one from .env.example")
                print(f"   Copy .env.example to .env and add your API keys")

    def _load_yaml(self):
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Please create workflow_config.yaml from the template."
            )

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        print(f"✅ Loaded configuration from {self.config_path}")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            section: Configuration section (e.g., 'extraction', 'processing')
            key: Configuration key within the section
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            config.get('extraction', 'target_folder_name', 'RFQ')
        """
        try:
            return self.config.get(section, {}).get(key, default)
        except (KeyError, AttributeError):
            return default

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.

        Args:
            section: Configuration section name

        Returns:
            Dictionary of section configuration
        """
        return self.config.get(section, {})

    def get_api_key(self) -> tuple:
        """
        Get API key from environment variables.

        Returns:
            Tuple of (api_key, key_type) where key_type is 'openrouter' or 'openai'

        Raises:
            ValueError if no API key is found
        """
        # Check for OpenRouter key first (recommended)
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            return openrouter_key, "openrouter"

        # Fall back to OpenAI key
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            return openai_key, "openai"

        # No key found
        raise ValueError(
            "❌ No API key found in environment variables!\n\n"
            "Please set one of the following:\n"
            "  - OPENROUTER_API_KEY (recommended)\n"
            "  - OPENAI_API_KEY\n\n"
            "Options:\n"
            "1. Create a .env file (copy from .env.example)\n"
            "2. Set environment variable:\n"
            "   Windows: set OPENROUTER_API_KEY=your-key\n"
            "   Linux/Mac: export OPENROUTER_API_KEY=your-key\n"
        )

    def should_use_openrouter(self) -> bool:
        """
        Determine if OpenRouter should be used based on config and available keys.

        Returns:
            True if OpenRouter should be used, False for direct OpenAI
        """
        # Check config preference
        use_openrouter = self.get('processing', 'use_openrouter', True)

        # If config says use OpenRouter, check if key is available
        if use_openrouter:
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
            if openrouter_key:
                return True
            else:
                print("⚠️  Config specifies OpenRouter but OPENROUTER_API_KEY not found")
                print("   Falling back to OpenAI (if available)")
                return False

        return False


# Global config instance (lazy loaded)
_config_instance: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """
    Get global configuration instance (singleton pattern).

    Returns:
        ConfigLoader instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance


def reload_config():
    """Reload configuration from files."""
    global _config_instance
    _config_instance = ConfigLoader()
    return _config_instance
