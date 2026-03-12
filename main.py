from agents.researcher import resercher
from agents.writer import writer
from agents.critic import critic
from agents.improver import improver

topic = input("Enter research topic: ")

state = {
    "topic": topic
}

# research
state.update(resercher(state))

# write report
state.update(writer(state))

while True:

    # critic evaluates
    state.update(critic(state))

    print("\nScore:", state["score"])
    print("Feedback:", state["feedback"])

    if state["score"] >= 9:
        break

    print("\nImproving report...\n")

    state.update(improver(state))

print("\nFINAL REPORT:\n")
print(state["report"])