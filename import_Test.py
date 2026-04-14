from sceneprogllm import LLM
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = LLM(response_format="text")
# response = llm("whiat is the capitial of France?")

## llm 자체의 시각 추론 테스트
# response = llm("what animal is shown in this iamge?", image_paths=["assets/lions.png"])

## VLM Spatial recognotion Test
response = llm("how many lions are there in this image?", image_paths=["assets/lions.png"])
print(response)

## limit of naive llm
## Hallucination 
## Lack of External Tools
## Compositionality Gaps
## Scale Dependence
## Limited Context
## Poor interpretability