import uuid
from config import load_environment
from agent.react_agent import agent

def chat_loop():
    prompt = "Please enter conversation ID (or press Enter to create a new one): "
    user_input = input(prompt)

    if not user_input:
        thread_id = str(uuid.uuid4())
    else:
        thread_id = user_input.strip()

    print(f"Using conversation ID: {thread_id}")
    print("Country Information Assistant started!")
    print("Type 'help' for capabilities or 'exit' to quit.")

    agent_config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            query = input("\nYou: ")

            if query.lower() in ["exit", "quit", "quitter"]:
                print("Bye!")
                break

            events = agent.stream(
                {"messages": [{"role": "user", "content": query}]},
                agent_config,
                stream_mode="values",
            )

            for event in events:
                if "messages" in event:
                    event["messages"][-1].pretty_print()

        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

if __name__ == "__main__":
    chat_loop()



