import os
from dotenv import load_dotenv
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# Removed external API tools to avoid API key requirements
# from crewai_tools import SerperDevTool, CrewaiEnterpriseTools
from problem_solving_research_agent.tools.file_writer import save_document_to_file
from problem_solving_research_agent.tools.google_docs import GoogleDocsCreatorTool, SimpleGoogleDocsCreatorTool

# Load environment variables
load_dotenv()


@CrewBase
class ProblemSolvingResearchAgentCrew:
    """ProblemSolvingResearchAgent crew"""

    
    @agent
    def problem_solving_research_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["problem_solving_research_specialist"],
            tools=[],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def document_publisher(self) -> Agent:
        return Agent(
            config=self.agents_config["document_publisher"],
            tools=[GoogleDocsCreatorTool()],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    

    
    @task
    def research_problem_and_create_solution_approach(self) -> Task:
        return Task(
            config=self.tasks_config["research_problem_and_create_solution_approach"],
        )
    
    @task
    def publish_solution_as_document(self) -> Task:
        return Task(
            config=self.tasks_config["publish_solution_as_document"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the ProblemSolvingResearchAgent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
