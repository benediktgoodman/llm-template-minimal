"""Asset and model configuration module for project-wide management using Pydantic.

This module provides a robust configuration system for managing paths, URIs,
and model settings across the project using Pydantic. It ensures type safety
and immutability of asset locations and model configurations.

Usage:
    1. Import the AssetConfig class and create an instance with your desired settings.
    2. Use the config instance throughout your project to access these settings.

Example:
    from confi_assets import AssetConfig

    config = AssetConfig(
        models_dir='/path/to/models',
        data_dir='gs://your-bucket/data',
        evaluations_dir='/path/to/evaluations',
        vectorstore_dir='gs://your-bucket/vectorstore',
        llm_model='openai-community/gpt2',
        tokenizer='sentence-transformers/all-MiniLM-L6-v2'
    )

"""
import os
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
from urllib.parse import urlparse

class AssetConfig(BaseModel):
    """Pydantic model for managing project-wide asset paths, URIs, and model settings.

    This class uses Pydantic to define and validate configuration parameters
    for various project assets and model settings. All attributes are read-only 
    and must be set upon instantiation.

    Attributes:
        models_dir (str): Path or URI to the models directory.
        data_dir (str): Path or URI to the data directory.
        evaluations_dir (str): Path or URI to the evaluations directory.
        vectorstore_dir (str): Path or URI to the vectorstore directory.
        llm_model (str): Name or path of the language model to use.
        tokenizer (str): Name or path of the tokenizer to use.
    """
    root_dir: str =  Field(default_factory=lambda: AssetConfig.find_project_root())
    models_dir: str = Field(..., description="Path or URI to the models directory")
    data_dir: str = Field(..., description="Path or URI to the data directory")
    evaluations_dir: str = Field(..., description="Path or URI to the evaluations directory")
    vectorstore_dir: str = Field(..., description="Path or URI to the vectorstore directory")
    llm_model: str = Field(..., description="Name or path of the language model to use")
    tokenizer: str = Field(..., description="Name or path of the tokenizer to use")
    
    # Ensures immutability of attributes in class
    model_config = {'frozen': True}
        
    @staticmethod
    def find_project_root() -> str:
        """Find the project root directory.

        This method searches for a pyproject.toml file in the current directory
        and its parents to determine the project root.

        Returns:
            str: The path to the project root directory.

        Raises:
            FileNotFoundError: If pyproject.toml is not found in the directory tree.
        """
        current_dir = Path.cwd()
        for _ in range(10):  # Limit to 10 levels up
            if 'pyproject.toml' in os.listdir(current_dir):
                return str(current_dir)
            current_dir = current_dir.parent
        raise FileNotFoundError("Could not find project root (pyproject.toml)")

    def is_cloud_uri(self, path: Optional[str] = None) -> bool:
        """Check if the given path or any path in the config is a cloud URI.

        This method can be used to determine if a specific path or any of the
        directory paths in the configuration are cloud URIs.

        Args:
            path: The path to check. If None, checks all directory paths in the config.

        Returns:
            bool: True if the path (or any directory path) is a cloud URI, False otherwise.
        """
        def _is_cloud_uri(p: str) -> bool:
            parsed = urlparse(p)
            return parsed.scheme in ['gs', 'gcs', 's3', 'azure']

        if path:
            return _is_cloud_uri(path)
        return any(_is_cloud_uri(p) for p in [self.models_dir, self.data_dir, self.evaluations_dir, self.vectorstore_dir])

