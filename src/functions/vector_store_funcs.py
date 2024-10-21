def format_docs(docs):
    """Formats a retrieved doc within a langchain llm chain"""
    return "\n\n".join(doc.page_content for doc in docs)