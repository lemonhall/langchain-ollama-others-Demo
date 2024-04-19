# python3 -m venv .venv
# source .venv/bin/activate
# pip install playwright
# playwright install
# pip install pytest-playwright
# pip install beautifulsoup4
# pip install lxml
# pip install langchain_community
# pip install langchain_core
# pip install langchain

# https://python.langchain.com/docs/integrations/toolkits/playwright

from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentType, initialize_agent

#同步加载游览器的工具
from langchain_community.tools.playwright.utils import (
    create_sync_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",      },
)



ollama_llm = ChatOllama(model="llama3")

sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()

agent_chain = initialize_agent(
    tools,
    ollama_llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
 
result = agent_chain.invoke("What are the headers on langchain.com?")
print(result)
