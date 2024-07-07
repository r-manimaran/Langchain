from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains import RetrievalQA

load_dotenv()

docs = [
    Document(
        page_content="Complex, Layered, rich red with dark fruit flavour",
        metadata={
            "name": "Opus One",
            "year": 2018,
            "rating":96,
            "grape":"Cabernet Sauvignon",
            "color": "red",
            "country":"USA"
        },
    ),
     Document(
        page_content="Luxurious, sweet wine with flavors of honey, apricot, and peach",
        metadata={"name":"Château d'Yquem", "year": 2015, "rating": 98, "grape": "Sémillon", "color":"white", "country":"France"},
    ),
    Document(
        page_content="Full-bodied red with notes of black fruit and spice",
        metadata={"name":"Penfolds Grange", "year": 2017, "rating": 97, "grape": "Shiraz", "color":"red", "country":"Australia"},
    ),
    Document(
        page_content="Elegant, balanced red with herbal and berry nuances",
        metadata={"name":"Sassicaia", "year": 2016, "rating": 95, "grape": "Cabernet Franc", "color":"red", "country":"Italy"},
    ),
    Document(
        page_content="Highly sought-after Pinot Noir with red fruit and earthy notes",
        metadata={"name":"Domaine de la Romanée-Conti", "year": 2018, "rating": 100, "grape": "Pinot Noir", "color":"red", "country":"France"},
    ),
    Document(
        page_content="Crisp white with tropical fruit and citrus flavors",
        metadata={"name":"Cloudy Bay", "year": 2021, "rating": 92, "grape": "Sauvignon Blanc", "color":"white", "country":"New Zealand"},
    ),
    Document(
        page_content="Rich, complex Champagne with notes of brioche and citrus",
        metadata={"name":"Krug Grande Cuvée", "year": 2010, "rating": 93, "grape": "Chardonnay blend", "color":"sparkling", "country":"New Zealand"},
    ),
    Document(
        page_content="Intense, dark fruit flavors with hints of chocolate",
        metadata={"name":"Caymus Special Selection", "year": 2018, "rating": 96, "grape": "Cabernet Sauvignon", "color":"red", "country":"USA"},
    ),
    Document(
        page_content="Exotic, aromatic white with stone fruit and floral notes",
        metadata={"name":"Jermann Vintage Tunina", "year": 2020, "rating": 91, "grape": "Sauvignon Blanc blend", "color":"white", "country":"Italy"},
    ),
]


embeddings = OpenAIEmbeddings()
print('Loading Chroma store...')

# Store the chroma db to local
persist_directory = 'db'
vectordb = Chroma.from_documents(docs, embeddings)
print('Chroma store loaded')

# Create Self quering Retriever
from langchain.retrievers import SelfQueryRetriever
from langchain_openai import OpenAI
from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_Info = [
    AttributeInfo(
        name="grape",
        description="The grape used to make the wine",
        type="string or list[string]"
    ), 
    AttributeInfo(
        name="rating",
        description="The Robert Parker rating for the wine 0-100",
        type="integer"
    ),
    AttributeInfo(
        name="year",
        description="The year the wine was made",
        type="integer"
    ),
    AttributeInfo(
        name="name",
        description="The name of the wine",
        type="string"
    ),
    AttributeInfo(
        name="color",
        description="The color of the wine",
        type="string or list[string]"
    ),
    AttributeInfo(
        name="country",
        description="The country of origin of the wine",
        type="string or list[string]"
    ),
]
document_content_description = "Brief description of the wine"

llm = OpenAI(temperature=0.0, verbose = True)

#create the retriever 
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectordb,
    document_content_description,
    metadata_field_Info,
    verbose=True
)

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    verbose=True
)


# response = retriever.get_relevant_documents(
#     "What are the different grape varieties used in the wines?",verbose=True
# )

response = chain.invoke(
    {
        "query": "List wine producing countries in the order of highest to lowest rating?",
    }
)

print(response)
