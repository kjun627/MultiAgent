from sceneprogllm import LLM
from rich.console import Console
from dotenv import load_dotenv

console = Console()
load_dotenv()
class Memory:
    def __init__(self, name, max_memory=1024):
        self.max_memory = max_memory
        self.name = name
        self.summarization_llm = LLM(system_desc=f"""
                                     your task is to briefly summarize the conversation history without losing important information.
                                     Try to keep the summary concise and to the point.
                                     """,
                                     response_format="text"
                                     )
        self.memeory = ""
        
    def compute_tokens(self, text):
        return len(text.split())
    
    def fetch(self):
        return self.memeory
    
    def commit(self, event):
        self.memory += event + "\n"

        if self.compute_tokens(self.memory) > self.max_memory:
            console.print(f"Memory exceeded for {self.name}. Summarizing...", style="yellow")
            summary =self.summarization_llm(self.memory)
            console.print(f"Current memory size: {self.compute_tokens(self.memory)} tokens", color="yellow")
            self.memory = summary
            
class SemanticMemory:
    def __init__(self, name):
        self.name = name
        import os
        from langchain_openai import OpenAIEmbeddings
        from langchain_chroma import Chroma
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))
        
        os.makedirs(f"./tmp", exist_ok=True)
        self.vector_store = Chroma(
            collection_name=self.name+"_vectorStore",
            embedding_function=embeddings,
            persist_directory=f"./tmp/{self.name}_vectorStore.db",
        )
        
    def build(self, files):
        from uuid import uuid4
        from langchain_core.documents import Document
        
        documents = []
        for path in files:
            with open(path, "r") as f:
                text = f.read()
                documents.append(Document(page_content=text, metadata={"source": path, "uuid":str(uuid4())}))
        
        self.vector_store.add_documents(documents)
        
    def fetch(self, query):
        results = self.vector_store.similarity_search(query, k = 1)
        tmp=[]
        for res in results:
            tmp.append(res.page_content)
        return "".join(tmp)