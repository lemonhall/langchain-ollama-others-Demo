#!/usr/bin/env python3
from typing import List, Tuple

from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI

#https://python.langchain.com/docs/integrations/toolkits/sql_database
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase

import os
import requests
import json

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


llm = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-xxxxxxxxxxxxxxxxx",
    model_name="moonshot-v1-8k",
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

agent_executor.invoke("取出notes表的title字段，然后由你来将这些题目做分类")
