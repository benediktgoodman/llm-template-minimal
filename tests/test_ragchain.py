import os
import pytest
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.llms import VLLM

script_path = os.getcwd()
for folder_level in range(50):
    if "pyproject.toml" in os.listdir(): 
        break
    os.chdir("../")
    
from src.config import asset_config  # noqa: E402
from src.functions.vector_store_funcs import format_docs

os.chdir(script_path)

@pytest.fixture(scope="module")
def setup_paths():
    script_path = os.getcwd()
    for folder_level in range(50):
        if "pyproject.toml" in os.listdir():
            break
        os.chdir("../")
    yield
    os.chdir(script_path)

@pytest.fixture(scope="module")
def llm(setup_paths):
    return VLLM(
        model=asset_config.llm_model,
        gpu_memory_utilization=0.4,
        download_dir=asset_config.models_dir,
    )

@pytest.fixture(scope="module")
def embedder(setup_paths):
    return HuggingFaceEmbeddings(
        model_name=asset_config.tokenizer,
        cache_folder=asset_config.models_dir,
    )

@pytest.fixture(scope="module")
def vector_store(embedder):
    return Chroma(
        collection_name="test",
        embedding_function=embedder,
    )

@pytest.fixture(scope="module")
def rag_chain(vector_store, llm):
    template = """Think step by step and use the following pieces of context to answer the users question.
    If you don't know the answer, just say that you don't know.
    ALWAYS return a "SOURCES" part in your answer.
    Context: {context}
    Question: {question}
    Helpful answer:
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"], template=template
    )
    return (
        {"context": vector_store.as_retriever(search_type='mmr', search_kwargs={'k': 1}) | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def test_vector_store_output(vector_store):
    mock_text = "This is a test document about artificial intelligence and machine learning."
    vector_store.add_texts([mock_text])
    
    query = "What is this document about?"
    results = vector_store.similarity_search(query, k=1)
    
    assert len(results) > 0, "No results returned from similarity search"
    assert results[0].page_content == mock_text, "Retrieved document does not match the added mock text"
    
    # Clean up
    #vector_store.delete([results[0].metadata['id']])

def test_rag_chain_output(rag_chain):
    response = rag_chain.invoke('What is AI?')
    
    assert isinstance(response, str), "RAG chain output is not a string"
    assert len(response) > 0, "RAG chain returned an empty response"
    #assert "SOURCES" in response, "RAG chain response does not include SOURCES"

    print(f"RAG Chain Response: {response}")
    
# def test_retrieval_in_prompt(vector_store, rag_chain):
#     # Add a specific document to the vector store
#     specific_text = "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems."
#     vector_store.add_texts([specific_text])
    
#     # Query the RAG chain with a related question
#     query = "What is the definition of AI?"
#     response = rag_chain.invoke(query)
    
#     # Check if the response contains information from the added document
#     assert "simulation of human intelligence" in response.lower(), "Response does not contain information from the retrieved document"
#     assert "SOURCES" in response, "Response does not include SOURCES"
    
#     print(f"Query: {query}")
#     print(f"RAG Chain Response: {response}")