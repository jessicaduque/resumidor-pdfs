from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from resumidor_pdfs.tools.custom_tool import PDFReaderTool

@CrewBase
class ResumidorPdfs():
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	pdfReader = PDFReaderTool(result_as_answer=True)

	@agent
	def pdf_reader_agent(self) -> Agent:
		return Agent(
			config = self.agents_config['pdf_reader_agent'],
			tools = [self.pdfReader], 
			verbose = True,
			allow_delegation = True
		)

	@agent
	def analyzer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['analyzer_agent'],
			verbose=True,
			allow_delegation = False
		)
	
	@agent
	def summarizer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['summarizer_agent'],
			verbose=True,
			allow_delegation = False
		)
	
	@agent
	def formatter_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['formatter_agent'],
			verbose=True,
			allow_delegation = False
		)
	
	@agent
	def quality_assurance_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['quality_assurance_agent'],
			verbose=True,
			allow_delegation = False
		)

	@task
	def read_pdf_task(self) -> Task:
		return Task(
			config=self.tasks_config['read_pdf_task']
		)

	@task
	def analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_task']
		)
	
	@task
	def summarize_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_task']
		)
	
	@task
	def format_task(self) -> Task:
		return Task(
			config=self.tasks_config['format_task']
		)
	
	@task
	def quality_assurance_task(self) -> Task:
		return Task(
			config=self.tasks_config['quality_assurance_task'],
			output_file='blog.md'
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True
		)
