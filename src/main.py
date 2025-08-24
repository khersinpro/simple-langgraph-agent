from config import load_environment
from agent.react_agent import agent

def chat_loop():
    agent_config = {"configurable": {"thread_id": "1"}}

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



