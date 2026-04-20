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
        