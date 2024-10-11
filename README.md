# team-ki-rag-template

A template repository for developing and testing LLM-based systems on Linux platforms.

## Overview

This repository provides a structured template for building LLM (Large Language Model) systems. It includes configuration management, model downloading, and a development environment setup using Poetry.

## Features

- Configurable asset and model management using Pydantic
- Automatic model downloading from Hugging Face
- Poetry for dependency management
- Pre-configured development tools (pytest, black, isort, pre-commit)

## Setup

1. Configure the system:
   - Open `src/config.py`
   - Modify the `AssetConfig` parameters to set your desired models and directories
   - You can use local paths or cloud URIs (e.g., GCS, S3) for storage locations

2. Run the setup script:
   ```bash
   bash setup.sh
   ```
   This script will:
   - Install Poetry
   - Install project dependencies
   - Prompt for your Hugging Face token and save it securely
   - Download the specified models

Note: This setup assumes a Linux environment. Additional steps may be required for other operating systems.

## Configuration

The `AssetConfig` class in `src/config_assets.py` manages paths and settings throughout the project. It supports both local and cloud storage:

- Local paths: Use standard file system paths
- Cloud URIs: Use URIs like `gs://bucket-name/path` for Google Cloud Storage

Example configuration in `src/config.py`:

```python
config = AssetConfig(
    llm_model='openai-community/gpt2',
    tokenizer='sentence-transformers/all-MiniLM-L6-v2',
    data_dir='gs://your-bucket/data',
    models_dir='/path/to/local/models',
    # ... other settings
)
```

Note: If using cloud storage, you'll need to add appropriate cloud SDK dependencies to `pyproject.toml` and set up authentication separately.

### Using the Configuration

To use the configuration in other modules or scripts, import it from `src/config.py`. Here's an example from `model_download.py`:

```python
from config import config

# Now you can use the config object
if config.is_cloud_uri(config.models_dir) is False:
    Path(config.models_dir).mkdir(exist_ok=True)

# Download models
snapshot_download(config.tokenizer, cache_dir=config.models_dir, token=hf_token)
snapshot_download(config.llm_model, cache_dir=config.models_dir, token=hf_token)
```

This approach ensures consistent configuration across your project.

## Project Structure

- `src/`: Source code directory
  - `config_assets.py`: Asset configuration using Pydantic
  - `config.py`: Main configuration file
  - `model_download.py`: Script for downloading models
- `tests/`: Test directory
- `pyproject.toml`: Poetry configuration and project metadata
- `setup.sh`: Setup script for easy project initialization

## Usage

After configuration and setup, you can start developing your LLM system using the provided structure. Use the `config` object from `src/config.py` to access paths and settings throughout your project.

## Development

- Use Poetry to manage dependencies: `poetry add package-name`
- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Sort imports: `poetry run isort .`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors

- Benedikt Goodman

For questions or support, please contact the contributors.
