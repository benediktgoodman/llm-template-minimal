import pytest
from vllm import LLM, SamplingParams
import os

@pytest.fixture(scope="module")
def llm():
    script_path = os.getcwd()
    for folder_level in range(50):
        if "pyproject.toml" in os.listdir():
            break
        os.chdir("../")
    from src.config import asset_config  # noqa: E402
    os.chdir(script_path)
    return LLM(asset_config.llm_model, download_dir=asset_config.models_dir, gpu_memory_utilization=0.9)

@pytest.fixture
def sampling_params():
    return SamplingParams(temperature=0.8, top_p=0.95)

def test_vllm_output(llm, sampling_params):
    prompts = [
        "Hello, my name is",
    ]
    
    outputs = llm.generate(prompts, sampling_params)
    
    assert len(outputs) == len(prompts), "Number of outputs should match number of prompts"
    
    for output, prompt in zip(outputs, prompts):
        assert output.prompt == prompt, f"Prompt mismatch for: {prompt}"
        assert len(output.outputs) > 0, f"No generated text for prompt: {prompt}"
        generated_text = output.outputs[0].text
        assert len(generated_text) > 0, f"Empty generated text for prompt: {prompt}"
        
        # Add more specific assertions based on expected output
        if prompt == "Hello, my name is":
            assert len(generated_text) > 0

        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")