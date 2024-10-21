import os
from pathlib import Path

script_path = os.getcwd()
for folder_level in range(50):
    if "pyproject.toml" in os.listdir(): 
        break
    os.chdir("../")
    
from src.functions.config_assets import AssetConfig  # noqa: E402
os.chdir(script_path)

# Looks for pyproject.toml, gets absolute path as string
root = Path(AssetConfig.find_project_root())

# Defaults to assume that we want to store everything in the image we are operating in
# Change to buckets if need be
# Kept private to prevent from being visible in linter elsewhere
_data_dir = root.joinpath('data').as_posix()
_llm_evals = root.joinpath('llm_evals').as_posix()
_vectorstore = root.joinpath('vectorstore').as_posix()
_models = root.joinpath('models').as_posix()

# config module we will be calling upon elsewhere
asset_config = AssetConfig(
    
    # Change these to change models in the system
    # Will affect which models are downloaded in model_download.py
    llm_model='openai-community/gpt2',
    tokenizer='sentence-transformers/all-MiniLM-L6-v2',
    
    # Root will always be a posix path
    root_dir=root.as_posix(),
    
    # These could be buckets if we want to
    data_dir=_data_dir,
    evaluations_dir=_llm_evals,
    vectorstore_dir=_vectorstore,
    models_dir=_models,   
)