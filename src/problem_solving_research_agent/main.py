#!/usr/bin/env python
import sys
from problem_solving_research_agent.crew import ProblemSolvingResearchAgentCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Get problem statement from user input
    print("🔍 Problem Solving Research Agent")
    print("=" * 40)
    problem_statement = input("Enter the problem statement you'd like me to research and solve: ").strip()
    
    if not problem_statement:
        print("❌ No problem statement provided. Exiting...")
        return
    
    print(f"\n🚀 Starting research for: {problem_statement}")
    print("-" * 60)
    
    inputs = {
        'problem_statement': problem_statement
    }
    ProblemSolvingResearchAgentCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    problem_statement = input("Enter the problem statement for training: ").strip()
    if not problem_statement:
        problem_statement = 'sample_value'
    
    inputs = {
        'problem_statement': problem_statement
    }
    try:
        ProblemSolvingResearchAgentCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ProblemSolvingResearchAgentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    problem_statement = input("Enter the problem statement for testing: ").strip()
    if not problem_statement:
        problem_statement = 'sample_value'
    
    inputs = {
        'problem_statement': problem_statement
    }
    try:
        ProblemSolvingResearchAgentCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
