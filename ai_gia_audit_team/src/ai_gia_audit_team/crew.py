from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import CSVSearchTool, PDFSearchTool, FileWriterTool

@CrewBase
class AuditCrew:
    """Audit crew for reviewing system access, transactions, and compiling reports."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    agent_llm = LLM(model="ollama/mistral")

    # Agents with tools instantiated directly
    @agent
    def logical_access_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['logical_access_reviewer'],
            tools=[CSVSearchTool(), FileWriterTool()],
            llm=self.agent_llm,
        )

    @agent
    def limit_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['limit_reviewer'],
            tools=[CSVSearchTool(), PDFSearchTool(), FileWriterTool()],
            llm=self.agent_llm,
        )

    @agent
    def transaction_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['transaction_reviewer'],
            tools=[CSVSearchTool(), PDFSearchTool(), FileWriterTool()],
            llm=self.agent_llm,
        )

    @agent
    def audit_trail_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['audit_trail_reviewer'],
            tools=[CSVSearchTool(), FileWriterTool()],
            llm=self.agent_llm,
        )

    @agent
    def audit_report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['audit_report_writer'],
            tools=[FileWriterTool()],
            llm=self.agent_llm,
        )

    # Tasks remain unchanged
    @task
    def review_logical_access(self) -> Task:
        return Task(
            config=self.tasks_config['review_logical_access'],
            agent=self.logical_access_reviewer(),
        )

    # ... (other task definitions remain the same)

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )