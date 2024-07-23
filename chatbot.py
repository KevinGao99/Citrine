from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
import openai
import guardrails as gd

guard = gd.Guard.from_rail_string(rail+str)

class ChatDoc:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="phi3")
        self.text_splitter = CharacterTextSplitter(
            separator="\n\n\n\n",
            chunk_size=20,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=True,
        )
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are a helpful chatbot for a bussiness. PLease follow the below Guidelines.
            1. Strictly Use the data present in the context for synthesising the answer.
            2. Focus on accuracy and relevance to the provided context
            3. Most important this is not to give too much information, answer in two to three sentences
            4. Do not use any information outside of the provided context
            5. Try to maintain the structure of sentence present in context
            6. Do not use any knowledge acquired outside of the provided context[/INST]
            </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    def check_retriever_output(self,text):
        print(f"**********\n{text}\n***********\n")
        if text["context"] == []:
            raise Exception("No Context Found")
        return text    
    
    def ingest(self, text_file_path: str):
        loader = TextLoader(text_file_path, encoding='utf-8')
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        # for ch in chunks:
        #     print(ch)
        #     print("\n")
        vector_store = Chroma.from_documents(chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,
                "score_threshold": 0.55,
            },
        )
        
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | RunnableLambda(self.check_retriever_output)
                      | self.prompt
                      | self.model
                      | StrOutputParser())

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a document first."
        try:
            return self.chain.invoke(query)
        except Exception as e:
            print(e)
            return "Sorry I could not help with this query!!"

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None

chat_bot = ChatDoc()
chat_bot.clear()
chat_bot.ingest("./test-document.txt")
chat_bot.ask("How can I start an account on Buffr")
