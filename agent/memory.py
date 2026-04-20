from sceneprogllm import LLM
from rich.console import Console

console = Console()

class Memory:
    def __init__(self, name, max_memeory=1024):
        self.max_memory = max_memeory
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