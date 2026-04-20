from sceneprogllm import LLM
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = LLM(response_format="text")

class BaseAgentCore:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        
        ##Core LLM Engeine
        self.synthesizer = LLM(system_desc=f"""
                                you are a helpful AI agent name {self.name}. Your role is
                                {self.role}. You are supposed to assist the user in achieving their goals."""
                                ,response_format="text")
        ## LLM to check user intent to terminate the session
        self.task_terminate = LLM( system_desc=f"""
                                    Based on the user's input, determine if the user wishes to end the session in
                                    case they don't have further queries. Return True if the session needs to end, otherwise return False.""",
                                    response_format="json",
                                    response_params={"complete":"bool"}
                                    )
        
        ## LLM to summaaarize the task
        self.task_summarizer = LLM( system_desc=f"""
                                    Your task is to go through the stdout of the execute code and generate a response
                                    for the intended task, for which the code was executed.""",
                                    response_format="text"
                                    )
    def __call__(self, input):
        response = self.synthesizer(input)
        return response, None
    
    def should_terminate (self, user_input):
        return self.task_terminate(user_input)["complete"]
    
    def summarize(self, input, response):
        prompt = f"""We trying to achieve the following task:{input} 
        Following is the response generated:{response}
        Plase summarize the output in light of the task. Be concise,
        don't haaaave to tell me about various tool calls, etc.
        I am looking for a direct answer to the task.
        Howevver, fell free to incloude intermediate resoning steps if they are there.
        If there is a response that the input requests, please incloude that in the response.
        Example response:"
        The product of 2 and 3 is 6"
        "Here is the summary of the text: ..."
        """
        response = self.task_summarizer(prompt)
        return response


## 실제 Agent 아키텍처는 LLM 객체를 역할별로 묶어서, 에이전트처럼 쓰려는거임.
## self.synthesizer 는 답변을 생성하는 메일 모델임. task_terminzate는 사용자가 대화를 끝내고 싶은지를 판별하는 모델
## 결과를 텍스트가 아니라 JSON으로 받고, True/false 형대로 답변을 받도록 함.
## 어떤 실행 결과나 stdout을 읽고 , 사용자가 원하는 답으로 요약하는 모델