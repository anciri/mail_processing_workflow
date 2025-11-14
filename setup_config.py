#!/usr/bin/env python3
"""
Configuration Setup Script
Helps you create workflow_config.yaml from the template with your settings.
"""
import os
import shutil
from pathlib import Path


def main():
    """Interactive setup for configuration files."""
    print("=" * 70)
    print("EMAIL WORKFLOW - CONFIGURATION SETUP")
    print("=" * 70)
    print()

    # Check for existing config
    config_file = Path("workflow_config.yaml")
    template_file = Path("workflow_config.yaml.template")
    env_file = Path(".env")
    env_example = Path(".env.example")

    # Setup workflow_config.yaml
    if config_file.exists():
        print(f"⚠️  {config_file} already exists.")
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Keeping existing configuration.")
        else:
            setup_yaml_config(template_file, config_file)
    else:
        setup_yaml_config(template_file, config_file)

    print()

    # Setup .env file
    if env_file.exists():
        print(f"⚠️  {env_file} already exists.")
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Keeping existing .env file.")
        else:
            setup_env_file(env_example, env_file)
    else:
        setup_env_file(env_example, env_file)

    print()
    print("=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Edit workflow_config.yaml with your Outlook settings")
    print("2. Edit .env with your API key")
    print("3. Run: python workflow.py")
    print()
    print("⚠️  SECURITY REMINDER:")
    print("   - Never commit workflow_config.yaml or .env to git")
    print("   - These files contain your personal information")
    print("   - They are already in .gitignore")
    print()


def setup_yaml_config(template_file, config_file):
    """Setup workflow_config.yaml from template."""
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        return

    print(f"\n📝 Creating {config_file} from template...")
    shutil.copy(template_file, config_file)
    print(f"✅ Created {config_file}")
    print()
    print("Please edit this file and set:")
    print("  - target_account_email: Your Outlook email")
    print("  - inbox_folder_name: Usually 'Inbox' or 'Bandeja de entrada'")
    print("  - target_folder_name: Your email folder name")
    print("  - target_subfolder_name: Optional subfolder (or leave empty)")


def setup_env_file(env_example, env_file):
    """Setup .env file from example."""
    if not env_example.exists():
        print(f"❌ Example file not found: {env_example}")
        return

    print(f"\n🔑 Creating {env_file} from example...")
    shutil.copy(env_example, env_file)
    print(f"✅ Created {env_file}")
    print()
    print("Please edit this file and set:")
    print("  - OPENROUTER_API_KEY: Your OpenRouter API key")
    print("  - OR OPENAI_API_KEY: Your OpenAI API key")
    print()
    print("Get API keys from:")
    print("  - OpenRouter: https://openrouter.ai/keys (recommended)")
    print("  - OpenAI: https://platform.openai.com/api-keys")


if __name__ == "__main__":
    main()
