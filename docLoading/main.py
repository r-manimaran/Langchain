from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()

#split the document into chunks
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(separator='\n',
                                      chunk_size=200,
                                       chunk_overlap=0)
loader = TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

#load in to Chroma db
from langchain.vectorstores.chroma import Chroma
db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="emb",
)

result = db.similarity_search("What is the interesting fact about the English language?")
print(result)