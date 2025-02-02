#!/usr/bin/env python3
import os
from typing import List, Tuple

from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI

#https://python.langchain.com/docs/integrations/toolkits/sql_database
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase

# https://python.langchain.com/docs/use_cases/sql/agents#next-steps
# 奥，对了，kimi暂时还不支持tools语法，算了。。。。。langchain还必须做适配才行
# https://platform.moonshot.cn/docs/intro#%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B
# https://github.com/MoonshotAI/MoonshotAI-Cookbook/blob/master/examples/langchain/main.py
# 参考这里
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     openai_api_base="https://api.moonshot.cn/v1/", 
#     openai_api_key="MOONSHOT_API_KEY",
#     model_name="moonshot-v1-8k",
# )

# print(llm.invoke("how can langsmith help with testing?"))
# 这么调用是可以的，但是就是不支持tools暂时



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

# sqlite> PRAGMA table_info(notes);
# 0|created_on|DATETIME|1||0
# 1|changed_on|DATETIME|1||0
# 2|id|INTEGER|1||1
# 3|title|VARCHAR(256)|0||0
# 4|content|TEXT|0||0
# 5|created_by_fk|INTEGER|1||0
# 6|changed_by_fk|INTEGER|1||0
# sqlite> 
db = SQLDatabase.from_uri("sqlite:///app.db")
#toolkit = SQLDatabaseToolkit(db=db)

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

agent_executor.invoke("取出notes表内所有的title字段的记录，然后由你来将这些题目做一个主题分类；最后，回答我，该数据库的主人可能的性格和爱好；")
