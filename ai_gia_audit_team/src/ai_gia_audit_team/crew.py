from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import CSVSearchTool, PDFSearchTool, FileReadTool, FileWriterTool

@CrewBase
class AuditCrew:
    """Audit crew for reviewing system access, transactions, and compiling reports."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    LLM_LLAMA31 = LLM(model="ollama/llama3.1")
    LLM_MISTRAL = LLM(model="ollama/mistral")
    LLM_PHI4=LLM(model="ollama/phi4")


    @agent
    def logical_access_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['logical_access_reviewer'],
            tools=[CSVSearchTool(), FileWriterTool()],  # Instantiate tools here
            llm=self.LLM_LLAMA31,  # Corrected reference to agent_llm
        )

    @agent
    def limit_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['limit_reviewer'],
            tools=[CSVSearchTool(), PDFSearchTool(), FileWriterTool()],  # Instantiate tools here
            llm=self.LLM_MISTRAL,  # Corrected reference to agent_llm
        )

    @agent
    def transaction_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['transaction_reviewer'],
            tools=[CSVSearchTool(), PDFSearchTool(), FileWriterTool()],  # Instantiate tools here
            llm=self.LLM_PHI4,  # Corrected reference to agent_llm
        )

    @agent
    def audit_trail_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['audit_trail_reviewer'],
            tools=[CSVSearchTool(), FileWriterTool()],  # Instantiate tools here
            llm=self.LLM_LLAMA31,  # Corrected reference to agent_llm
        )

    @agent
    def audit_report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['audit_report_writer'],
            tools=[FileWriterTool()],  # Instantiate tools here
            llm=self.LLM_MISTRAL,  # Corrected reference to agent_llm
        )

    @task
    def review_logical_access(self) -> Task:
        return Task(
            config=self.tasks_config['review_logical_access'],
            agent=self.logical_access_reviewer(),
        )

    @task
    def review_transaction_limits(self) -> Task:
        return Task(
            config=self.tasks_config['review_transaction_limits'],
            agent=self.limit_reviewer()
        )

    @task
    def review_transactions(self) -> Task:
        return Task(
            config=self.tasks_config['review_transactions'],
            agent=self.transaction_reviewer()
        )

    @task
    def review_audit_trail(self) -> Task:
        return Task(
            config=self.tasks_config['review_audit_trail'],
            agent=self.audit_trail_reviewer()
        )

    @task
    def compile_audit_report(self) -> Task:
        return Task(
            config=self.tasks_config['compile_audit_report'],
            agent=self.audit_report_writer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            manager_llm=self.LLM_LLAMA31
        )