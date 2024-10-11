# We will use poetry for managing dependencies
pip3 install poetry

# Installs requirements
poetry install

# Prompt for the Hugging Face token
read -p "Enter your Hugging Face token: " hf_token

# Append the token to the .env file in the home directory
echo "HUGGINGFACE_TOKEN=$hf_token" >> ~/.env

# Set restrictive permissions on the file
chmod 600 ~/.env

echo "Hugging Face token has been appended to ~/.env"
echo "You can access it in your Python scripts using python-dotenv and os.getenv()"

# Downloads model and scraped data
python3 src/model_download.py
pytest tests/test_cuda_availability.py