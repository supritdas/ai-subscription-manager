import asyncio

from agents import Runner

from database import initialize_database
from agent import subscription_agent


async def main():
    initialize_database()

    print("=" * 50)
    print("       AI SUBSCRIPTION MANAGER")
    print("=" * 50)

    print("\nType 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            result = await Runner.run(
                subscription_agent,
                user_input,
            )

            print(f"\nAgent: {result.final_output}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())