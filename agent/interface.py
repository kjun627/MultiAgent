from agent.agent import BaseAgentCore
from rich.console import Console

console = Console()

class Agent252DBase:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.core = BaseAgentCore(name, role)
    
    def build_context(self, user_input):
        context = f"""
        User: {user_input}
        Use the following context to answer the user's query.
        """
        return context
    
    def generate_response(self, user_input):
        input = self.build_context(user_input)
        response, _ = self.core(input)
        return response, None
    
    def __call__(self, input, caller="User"):
        console.print(f"{caller}: {input}", style="yellow")
        if self.core.should_terminate(input):
            console.print(f"{self.name}: Task complete.", style="green")
            return False
        
        else:
            response, _ = self.generate_response(input)
        
        summary = self.core.summarize(input, response)
        console.print(f"{self.name}: {summary}", style='blue')
        return summary
    
    def run(self):
        while True:
            query = input("User Input: ")
            response = self(query, caller="User")
            
            if not response:
                break

class Agent252DWithMemory(Agent252DBase):
    def __init__(self, name, role):
        super().__init__(name, role)
        from agent.memory import Memory
        from agent.memory import SemanticMemory
        self.chat_history = Memory(name=self.name+"_chat_history", max_memory=1024)
        self.semantic_memory = SemanticMemory(name=self.name+'_semantic_memory')
        self.semantic_memory.build(["rag_ex/india-france.txt", "rag_ex/india-capital.txt"])
        
    def build_context(self, user_input):
        context = self.chat_history.fetch()
        retrieved_context = self.semantic_memory.fetch(user_input)
        context=f"""
        Interaction history:
        {context}
        Use the following context to answer the user's query.
        {retrieved_context}
        """
        return context
    
    def __call__(self, input, caller="User"):
        console.print(f"{caller}: {input}", style="yellow")
        self.chat_history.commit(f"{caller}: "+ input)
        
        if self.core.should_terminate(input):
            self.chat_history.commit("Task complete.")
            console.print(f"{self.name}: Task complete.", style="green")
            return False
        
        else:
            response, code = self.generate_response(input)
            
        summary = self.core.summarize(input.response)
        self.chat_history.commit(f"{self.name}: {summary}")
        console.print(f"{self.name}: {response}", style='blude')
        
        return summary