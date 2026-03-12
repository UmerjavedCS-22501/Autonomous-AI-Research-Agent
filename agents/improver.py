from llm import llm

def improver(state):

    report = state["report"]
    feedback = state["feedback"]

    prompt = f"""
    Improve the research report using the feedback.

    Report:
    {report}

    Feedback:
    {feedback}

    Make the report clearer, deeper, and more professional.
    """

    response = llm.invoke(prompt)

    return {
        "report": response.content
    }