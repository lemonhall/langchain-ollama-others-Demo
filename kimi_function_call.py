from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.messages import HumanMessage
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_community.chat_models import ChatOpenAI
import json

search = DuckDuckGoSearchRun()

model = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx",
    model_name="moonshot-v1-8k",
)

model2 = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxx",
    model_name="moonshot-v1-8k",
)

model = model.bind(
    functions=[
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, " "e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["location"],
            },
        }
    ],
    function_call={"name": "get_current_weather"},
)

# 使用 JsonOutputToolsParser 来试图解析结果
# https://python.langchain.com/docs/modules/model_io/chat/function_calling#binding-functions

# tool_chain = model | JsonOutputToolsParser(name="get_current_weather")
# result = tool_chain.invoke("what is the weather in Boston?")
# print(result)
# 这个方法是废的，因为这是针对OpenAI的
def get_current_weather(location):
    res = "真的是在被call哦，get_current_weather:"+location
    print(res)
    result = search.run("what is the current weather in "+location)
    return result

result = model.invoke("what is the weather in 西安?")
# 判断字符串是否是可调用的函数
#https://stackoverflow.com/questions/59912800/how-do-i-check-if-a-string-is-a-callable-name-in-python
function_call_name = result.additional_kwargs['function_call']['name']
function_call_arguments = result.additional_kwargs['function_call']['arguments']

if callable(locals()[function_call_name]):
    print(f"{function_call_name} 是当前文件中可调用的函数。")
    location_object = json.loads(function_call_arguments)
    location = location_object["location"]
    print("location:",location)
    res = eval(function_call_name)(location)
    result = model2.invoke(res+"\n\n 根据上下文，并且使用celsius来说明，使用Chineses来总结，这个城市的天气是怎样的？")
    print(result)
else:
    print(f"{function_call_name} 不是当前文件中可调用的函数。")
