from llm import llm

def writer(state):
    topic=state["topic"]
    source=state["source"]

    prompt=f"""
    write the detail research report on the topic :{topic}
    use the following information :
    {source}
    the report must include:

    - introduction
    - Key component
    - applications
    - feature trends
    """
    responce=llm.invoke(prompt)
    return{
        "report":responce.content
    }
        