from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.document_loaders import TextLoader
import gradio as gr

load_dotenv()


def test_llm():
    llm = OpenAI(temperature=0.9)
    text = "What would be a good company name for a company that makes colorful socks?"
    print(llm(text))
    
    
def test_chat(message: str = "Hello, how are you?"):
    chat = ChatOpenAI(temperature=0, max_tokens=1000)
    messages = [
        SystemMessage(content="You are a helpful assistant that translates English to French."),
        HumanMessage(content=message)
    ]
    print(chat(messages).content)


def test_vector_search():
    loader = TextLoader('../../../state_of_the_union.txt')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    qdrant = Qdrant.from_documents(
        docs, embeddings,
        path="/tmp/local_qdrant",
        collection_name="my_documents",
    )
    

def greet(name):
    return "Hello " + name + "!"
 
    
def llm_io(input_text):
    llm = OpenAI(temperature=0.9)
    return llm(input_text)


if __name__ == "__main__":
    test_chat()
    # demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    # demo.launch()  
    
