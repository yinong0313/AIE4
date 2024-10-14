from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_community.llms import VLLMOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from operator import itemgetter
from langchain.schema.output_parser import StrOutputParser
from pydantic import BaseModel, Field
from langchain.schema.runnable import RunnablePassthrough
from typing import Any, List, Union

app = FastAPI()

llm = OllamaLLM(
    model="qwen2:1.5b",  
    base_url="http://localhost:11434", 
)

RAG_PROMPT_TEMPLATE = """\
<|start_header_id|>system<|end_header_id|>
You are a helpful assistant. You answer user questions based on provided context. If you can't answer the question with the provided context, say you don't know.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
User Query:
{query}

Context:
{context}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

rag_prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

embeddings = OllamaEmbeddings(
    model="snowflake-arctic-embed:22m",
)

qdrant_vectorstore = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="legal_data",
    url="http://localhost:6333",
)

retriever = qdrant_vectorstore.as_retriever()

lcel_rag_chain = {"context": itemgetter("query") | retriever, "query": itemgetter("query")}| rag_prompt | llm

class Input(BaseModel):
    query: str

class Output(BaseModel):
    output: Any

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(
    app, 
    lcel_rag_chain.with_types(input_type=Input, output_type=Output).with_config(
        {"run_name" : "legal_data_rag"}
    )
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
