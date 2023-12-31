import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

import chromadb
from pathlib import Path
from llama_index import download_loader
from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index import StorageContext
from llama_index.llms import OpenAI

# 加载pdf文档
PDFReader = download_loader('PDFReader')
loader = PDFReader()
documents = loader.load_data(file=Path('/Users/shirley/Documents/Apps/chroma/绩效管理的定义.pdf'))


# 文档分块，指定llm
service_context = ServiceContext.from_defaults(chunk_size=500, llm=OpenAI())

# 自定义向量存储
chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.create_collection('llamaindex_test1')
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 创建索引
index = VectorStoreIndex.from_documents(documents,
                                        service_context=service_context,
                                        storage_context=storage_context)

# 指定响应模式，启用流式响应，默认llm为openai
query_engine = index.as_query_engine(response_mode='tree_summarize', streaming=True)
response = query_engine.query("什么是绩效管理？")
response.print_response_stream()

