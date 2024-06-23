import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings


import tempfile
import whisper
from pytube import YouTube

from operator import itemgetter

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=cdiD-9MMpb0"

model = ChatOpenAI(
    temperature=0,
    openai_api_key=OPENAI_API_KEY,
    verbose=True,
    max_tokens=1000,
)
'''
#commented code 

model.invoke("What MLB team won the wword series during COVID-19 pandemic?")

parser = StrOutputParser()
chain = model | parser
response =chain.invoke("What MLB team won the wword series during COVID-19 pandemic?")
print(response)

'''

parser = StrOutputParser()

template = """
Answer the question based on the context below. If you don't know the answer, reply I don't know
Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
prompt.format(context="Mary's sister is Susana", question="Who is Mary's sister?")

chain = prompt | model | parser
'''
response2 = chain.invoke({"context": "Mary's sister is Susana", "question": "Who is Mary's sister?"})
print(response2)
'''

#combining chains
translation_prompt = ChatPromptTemplate.from_template(
    "Translate {answer} to {language}"
)

translation_chain = (
    {"answer":chain, "language":itemgetter("language")} | translation_prompt | model | parser
)
'''
response3 = translation_chain.invoke(
    {
        "context":"Mary's sister is Susana. She does not have any more siblings.",
        "question":"How many sisters does Mary have?",
        "language":"Spanish"
    })
print(response3)
'''
# use the Entire Transcript as context
if not os.path.exists("transcript.txt"):
    youtube = YouTube(YOUTUBE_VIDEO)
    audio = youtube.streams.filter(only_audio=True).first()

    #lets load the base model. This is not the most accurate model but it is good enough for this example
    whisper_model = whisper.load_model("base")

    with tempfile.TemporaryDirectory() as temp_dir:
        file = audio.download(output_path=temp_dir)
        transcription = whisper_model.transcribe(file,fp16=False)["text"].strip()

        with open("transcript.txt", "w") as f:
            f.write(transcription)

with open("transcript.txt", "r") as file:
    transcription = file.read()

transcription[:100]
'''
try:
    response = chain.invoke({
        "context":transcription,
        "question":"Is reading papers a good idea?"
    }
    )
    print(response)
except Exception as e:
    print(e)

'''
loader = TextLoader("transcript.txt")
documents = loader.load()
#print(documents[0])
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs = text_splitter.split_documents(documents)
#print(docs)

embeddings = OpenAIEmbeddings()
embeddings_query = embeddings.embed_query("Who is Mary's sister?")
print(f'Embeddings Length:{len(embeddings_query)}')
print(embeddings_query[:10])

sentence1 =embeddings.embed_query("Mary's sister is Susana")
sentence2 =embeddings.embed_query("Pedro's mother is a teacher")

#using Cosine Similarity to find the similarity between the two sentences
from sklearn.metrics.pairwise import cosine_similarity
query_sentence1_similarity = cosine_similarity([embeddings_query],[sentence1])[0][0]
query_sentence2_similarity = cosine_similarity([embeddings_query], [sentence2])[0][0]
print(f'Cosine Similarity between the query and the first sentence:{query_sentence1_similarity}')
print(f'Cosine Similarity between the query and the second sentence:{query_sentence2_similarity}')


# setting up vector Stores
from langchain_community.vectorstores import DocArrayInMemorySearch
vector_store1 = DocArrayInMemorySearch.from_texts(
    [
        "Mary's sister is Susana.",
        "John and Tommy are brothers",
        "Patrica likes white cars",
        "Pedro's mother is a teacher",
        "Lucia drives an audi",
        "Mary has two sibilings"
    ],   
    embedding=embeddings
    
)
# Now qquery is vectorStore1
res =vector_store1.similarity_search_with_score(query="Who is Mary's sister",k=3)
print(res)

retriever1 = vector_store1.as_retriever()
print(retriever1.invoke("Who is Mary's sister?"))

print("-------------------")
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
setup = RunnableParallel(context= retriever1, question = RunnablePassthrough())
setupRespose = setup.invoke("What color is Patricia's car?")
print(setupRespose)
'''
# now pass it to chain
chain = setup | prompt | model | parser
resp1= chain.invoke("What color is Patricia's car?")
print(resp1)

resp2 = chain.invoke("hat car does Lucia drive?")
print(resp2)
'''

# Now use the transcript to load to vector store
vector_store2 = DocArrayInMemorySearch.from_documents(
    docs,
    embedding=embeddings
)
retriever2 = vector_store2.as_retriever()   
chain =(
    {"context":retriever2, "question":RunnablePassthrough()}
      | prompt | model | parser
)
'''
transResponse = chain.invoke("What is synthentic intelligence")
print(transResponse)
'''
#setting up Pinecone instead of in memory vector store
from langchain_pinecone import PineconeVectorStore
index_name = "trans-rag-index"
vector_store3 = PineconeVectorStore.from_documents(
    docs,
    embedding=embeddings,
    index_name=index_name
)
retriever3 = vector_store3.as_retriever()
pineresponse = vector_store3.similarity_search("What is Hollywood going to start doing?")[:3]

## print(f'PineConeResponse:{pineresponse}')

# Now pass the retriever to the chain
chain =(
    {"context":retriever3, "question":RunnablePassthrough()}
      | prompt | model | parser
)

transResponse1 = chain.invoke("What is Hollywood going to start doing?")
print(transResponse1)


