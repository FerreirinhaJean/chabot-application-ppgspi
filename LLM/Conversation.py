import os
from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from .Constants import PROMPT_TEMPLATE


class Conversation:
    def __init__(self, temperature=0, verbose=True):
        load_dotenv()
        self.__verbose = verbose
        self.__PATH_VECTOR_STORE = os.getenv('PATH_VECTOR_STORE')

        self.__embeddings = OpenAIEmbeddings(
            deployment=os.getenv('OPEN_AI_EMBEDDING_NAME')
        )

        self.__llm = AzureChatOpenAI(
            temperature=temperature,
            deployment_name=os.getenv('OPEN_AI_MODEL_NAME'),
            request_timeout=600,
            verbose=verbose
        )

        self.__vector = FAISS.load_local(self.__PATH_VECTOR_STORE, self.__embeddings)

    def __store_vector(self, clean_pages):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=1200,
            length_function=len
        )

        documents_split = splitter.split_text(clean_pages)
        documents = splitter.create_documents(documents_split)

        vector_store = FAISS.from_documents(documents, self.__embeddings)
        vector_store.save_local("vector")

    # def __load_vector(self):
    #     return FAISS.load_local(self.__PATH_VECTOR_STORE, self.__embeddings)

    def create_load_qa(self):
        prompt_template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=['context', 'chat_history', 'question']
        )

        memory_chat = ConversationBufferMemory(memory_key='chat_history', input_key='question')

        chain_qa = load_qa_chain(
            llm=self.__llm,
            chain_type='stuff',
            memory=memory_chat,
            verbose=self.__verbose,
            prompt=prompt_template
        )

        return chain_qa

    def process_run_qa(self, question, chain_qa):
        context = self.__vector.similarity_search(question)
        return chain_qa.run(input_documents=context, question=question)
