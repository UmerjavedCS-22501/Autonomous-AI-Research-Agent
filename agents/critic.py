from llm import llm
import json
import re

def critic(state):

    report = state["report"]

    prompt = f"""
    Evaluate the research report.

    Give a score from 1 to 10.

    Respond ONLY in this format:

    score: <number>
    feedback: <text>

    Report:
    {report}
    """

    response = llm.invoke(prompt)

    text = response.content

    try:
        score = int(re.search(r"score:\s*(\d+)", text).group(1))
        feedback = re.search(r"feedback:\s*(.*)", text).group(1)

    except:
        score = 6
        feedback = "Improve clarity and add more details."

    return {
        "score": score,
        "feedback": feedback
    }