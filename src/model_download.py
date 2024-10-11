from huggingface_hub import snapshot_download, login
import os
from dotenv import load_dotenv
from pathlib import Path

from config import asset_config

# Loads env where we can get hf_token saved by user
load_dotenv()

# Makes sure download folder exists if we're working locally
if asset_config.is_cloud_uri(asset_config.models_dir) is False:
    Path(asset_config.models_dir).mkdir(exist_ok=True)

# Gets hf-token from dotenv
hf_token = os.getenv('HUGGINGFACE_TOKEN')

# Login in case of using protected models
login(token=hf_token, add_to_git_credential=True)

# Download models
snapshot_download(asset_config.tokenizer, cache_dir=asset_config.models_dir, token=hf_token)
snapshot_download(asset_config.llm_model, cache_dir=asset_config.models_dir, token=hf_token)
