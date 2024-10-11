from huggingface_hub import snapshot_download, login
import os
from dotenv import load_dotenv
from pathlib import Path

from config import config

# Loads env where we can get hf_token saved by user
load_dotenv()

# Makes sure download folder exists if we're working locally
if config.is_cloud_uri(config.models_dir) is False:
    Path(config.models_dir).mkdir(exist_ok=True)

# Gets hf-token from dotenv
hf_token = os.getenv('HUGGINGFACE_TOKEN')

# Login in case of using protected models
login(token=hf_token, add_to_git_credential=True)

# Download models
snapshot_download(config.tokenizer, cache_dir=config.models_dir, token=hf_token)
snapshot_download(config.llm_model, cache_dir=config.models_dir, token=hf_token)
