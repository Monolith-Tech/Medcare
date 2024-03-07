from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from langchain_community.document_loaders import TextLoader

loader = TextLoader("../../modules/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = Weaviate.from_documents(docs, embeddings, weaviate_url=WEAVIATE_URL, by_text=False)

query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)

print(docs[0].page_content)

