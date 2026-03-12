from langchain_community.tools import DuckDuckGoSearchRun


search=DuckDuckGoSearchRun()

def web_search(query:str):
    result=search.run(query)
    return result


