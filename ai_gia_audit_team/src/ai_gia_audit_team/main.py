import os
from crew import AuditCrew

# Set up environment variables for API keys if needed
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Instantiate the crew
audit_crew = AuditCrew()

# Kickoff the crew's work
result = audit_crew.crew().kickoff()

print("Audit Report:")
print(result)