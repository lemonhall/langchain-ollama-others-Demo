import os
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

# -----------------------------------------------------------------------------
# 使用 PowerShell
# 打开 PowerShell（在 “开始” 菜单中搜索 “PowerShell” 并打开）。
# 要为当前用户设置环境变量，可以使用
# $env:SILICONFLOW_API_KEY = "your_api_key"
# 命令。
# 同样，将"your_api_key"替换为实际的 API 密钥。不过，这种方式设置的环境变量只在当前 PowerShell 会话中有效。

# 要永久设置环境变量（对于当前用户），可以使用
# [Environment]::SetEnvironmentVariable("SILICONFLOW_API_KEY","your_api_key","User")。
# 如果要设置系统级别的环境变量（需要管理员权限），可以将最后一个参数改为"Machine"，
# 例如
# [Environment]::SetEnvironmentVariable("SILICONFLOW_API_KEY","your_api_key","Machine")。
# Set up SILICONFLOW API key
# 记得使用以上方法后，需要关闭vscode后重启vscode，之后点击F5运行python脚本的时候才能生效
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY')

if not SILICONFLOW_API_KEY:
    raise ValueError("SILICONFLOW API key is not set. Please set the SILICONFLOW_API_KEY environment variable.")

llm = ChatOpenAI(
    openai_api_base="https://api.siliconflow.cn/v1", 
    openai_api_key= SILICONFLOW_API_KEY,
    model_name="deepseek-ai/DeepSeek-V3",
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
