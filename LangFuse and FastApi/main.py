import datetime
from operator import itemgetter

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.docstore.document import Document
from langfuse import Langfuse
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from contextlib import asynccontextmanager

load_dotenv()
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "chatusers"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def verify_password(self, password:str):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

embeddings = OpenAIEmbeddings()

store = PGVector(
    collection_name="pgcollection",
    connection_string=DATABASE_URL,
    embedding_function=embeddings,
)
store.add_documents([Document(page_content="Pizza Margherita costs 5 dollars")])
retriever = store.as_retriever()

template ="""
Answer the question based only on the following context:
{context}
Always speak to the user with his/her name:{name}. Never forgot the user's name. Like "Hello Tom"
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()

chain =(
    {
        "context":itemgetter("question") | retriever,
        "question":itemgetter("question"),
        "name":itemgetter("name"),
    }
    | prompt
    | model
    | output_parser
)

#FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = "your_secret_key"

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        return False
    return user

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_langfuse():
    return Langfuse()

def get_trace_handler(langfuse:Langfuse = Depends(get_langfuse), user=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    trace = langfuse.trace(user_id = user.username
    )
    return trace.get_langchain_handler()

#endpoints
@app.post("/register", response_model=UserOut)
def register(user_in: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=user_in.username, hashed_password=hashed_password.decode('utf-8'))
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=user.id, username=user.username)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/ask")
async def ask(question: str, user=Depends(get_current_user), trace_handler = Depends(get_trace_handler)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    query = {"question":question, "name":user.username}

    result = await chain.ainvoke(query, config ={"callbacks": [trace_handler]})
    return result

if "__name__"=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)