#!/usr/bin/env python3
from typing import List, Tuple

from langchain.chains import ConversationChain
#https://python.langchain.com/docs/integrations/toolkits/sql_database
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama

ollama_llm = ChatOllama(model="llama3")

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
    llm=ollama_llm,
    db=db,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# agent_executor.invoke("请列出notes表里从标题来分类，你觉得有可能是菜谱的记录")
agent_executor.invoke("""取出notes表的title字段，然后由你来根据这些title字段的来猜测哪一些有可能是菜谱""")
