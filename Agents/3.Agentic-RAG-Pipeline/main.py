import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline


def load_docs_from_folder(folder_path):
    """Load PDF documents from a folder."""
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, filename))
            docs.extend(loader.load())
    return docs


def agent_controller(query):
    """Determine whether to search documents or answer directly."""
    q = query.lower()
    if any(word in q for word in ["pdf", "document", "data", "summarize", "information", "find"]):
        return "search"
    return "direct"


def rag_pipeline(query, retriever, llm):
    """RAG pipeline that routes queries based on agent decision."""
    action = agent_controller(query)
    if action == "search":
        print(f"Agent decided to SEARCH document for query: {query}")
        relevant_docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"Using the following context: {context}\nAnswer the question: {query}"
    else:
        print(f"Agent decided to DIRECTLY ANSWER query: {query}")
        prompt = query
    response = llm(prompt)[0]['generated_text']
    return response


def main():
    print("Hello from agentic-rag-pipeline!")
    
    # Load documents from docs folder
    docs = load_docs_from_folder("docs")
    print(f"Loaded {len(docs)} pages from the PDF.")

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = text_splitter.split_documents(docs)
    print(f"Split {len(chunks)} chunks.")

    # Create embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Save the embeddings to a vector store
    texts = [chunk.page_content for chunk in chunks]
    db = Chroma(
        collection_name="pdf_docs", 
        embedding_function=embedding_model
    )
    db.add_texts(texts)
    print("Embeddings stored in Chroma vector store.")

    # Retrieve relevant documents
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Local LLM
    llm = pipeline("text2text-generation", model="google/flan-t5-small", max_length=150)

    # Test 1: A document related query
    query1 = "Summarize the key points from the documents."
    response1 = rag_pipeline(query1, retriever, llm)
    print(f"Response to Query 1: {response1}")

    # Test 2: A general knowledge query
    query2 = "What is the capital of France?"
    response2 = rag_pipeline(query2, retriever, llm)
    print(f"Response to Query 2: {response2}")


if __name__ == "__main__":
    main()
