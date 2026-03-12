from tools.search_tool import web_search


def resercher(state):
    
    topic=state["topic"]

    results=web_search(topic)

    return{
        "source":results
    }