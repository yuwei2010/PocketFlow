from .flow import create_joke_flow

def main():
    """Main function to run the joke generator application."""
    print("Welcome to the Command-Line Joke Generator!")

    # Initialize the shared store as per the design
    shared = {
        "topic": None,
        "current_joke": None,
        "disliked_jokes": [],
        "user_feedback": None
    }

    # Create the flow
    joke_flow = create_joke_flow()

    # Run the flow
    joke_flow.run(shared)

    print("\nThanks for using the Joke Generator!")

if __name__ == "__main__":
    main() 