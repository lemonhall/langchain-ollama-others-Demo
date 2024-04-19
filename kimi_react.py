from langchain import hub
from langchain.agents import AgentExecutor, load_tools
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    ReActJsonSingleInputOutputParser,
)
from langchain.tools.render import render_text_description
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
import random

@tool("random_number", return_direct=False)
def get_random_number() -> int:
    """Returns a random number between 0-100."""
    rn = random.randint(0, 100)
    print("\n我真的用python代码去call出来一个随机数哈：",rn)
    return rn

llm = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-xxxxxxxxxxxxxxxx",
    model_name="moonshot-v1-8k",
)

# loading langchin llm-math tool and appending our custom tool too, 
# ReAct will use both the tools
tools = load_tools(["llm-math"], llm=llm)
tools.append(get_random_number)

# setup ReAct style prompt
prompt = hub.pull("hwchase17/react-json")
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

# define the agent
chat_model_with_stop = llm.bind(stop=["\nFinal Answer"])
print("当下的prompt内容是：")
print(prompt)
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | chat_model_with_stop
    | ReActJsonSingleInputOutputParser()
)

# instantiate AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

agent_executor.invoke(
    {
    "input": "First get a random number and then calculate its value multiplied by 3?"
    }
)
