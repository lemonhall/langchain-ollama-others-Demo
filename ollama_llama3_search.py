# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain.globals import set_verbose

set_verbose(True)

search = DuckDuckGoSearchRun()
ollama_llm = ChatOllama(model="llama3")

# # 这里就是一个能成功运行的例子了
# prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
# prompt_value = prompt.invoke({"topic": "ice cream"})
# print(prompt_value)

# model = ollama_llm

# message = model.invoke(prompt_value)
# print(message)

# output_parser = StrOutputParser()

# chain = prompt | model | output_parser

# chain.invoke({"topic": "ice cream"})

# template = """turn the following user input into a search query for a search engine:{input}"""
# prompt = ChatPromptTemplate.from_template(template)
# prompt_value = prompt.invoke({"input": "哈马斯到底能否赢得2023年底的这场战争？"})
# print("============================== \n print(prompt_value):")
# print(prompt_value)
# print("============================== END of print(prompt_value):")
# model = ollama_llm
# message = model.invoke(prompt_value)
# print(message)
# result = search.run("哈马斯 2023年底 战争 赢得可能性")

# 第一段：组装出一个prompt value
template = """并且将以下用户输入变为搜索引擎的关键词，
回答务必简短，不要大段大段的推演过程，只给出搜索用的关键词，不要其它提示词:{input}"""
prompt = ChatPromptTemplate.from_template(template)
prompt_value = prompt.invoke({"input": "what is hamas"})
print("============================== \n print(prompt_value):")
print(prompt_value)
print("============================== END of print(prompt_value):")
# 第二段：输出给LLM，拿到BaseMessage
model = ollama_llm
llm_result = model.invoke(prompt_value)
print("============================== \n print(llm_result):这里的返回应该是一个BaseMessage")
print(llm_result)
print("============================== END of print(llm_result):")
# 第三段：把BaseMessage输出给StrOutputParser，拿到纯String
output_parser = StrOutputParser()
parser_result = output_parser.invoke(llm_result)
print("============================== \n print(parser_result):这里的返回应该是一个str")
print(parser_result)
print("============================== END of print(parser_result):")
# 第四段：将纯String输出给DDg，拿到输出
result = search.run(parser_result)
print(result)

# # 第五段：试图链化
# template = """将如下用户输入变为搜索引擎的关键词，回答务必简短，不要大段大段的推演过程，只要关键词的输出:{input}"""
# prompt = ChatPromptTemplate.from_template(template)
# model = ollama_llm
# output_parser = StrOutputParser()
# chain = prompt | model | StrOutputParser() | search
# chain.invoke({"input": "亚伦.布什内尔是谁?"})
