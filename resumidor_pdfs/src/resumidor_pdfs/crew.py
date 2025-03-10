from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from resumidor_pdfs.tools.custom_tool import PDFReaderTool, TextSections
from dotenv import load_dotenv
import os

load_dotenv()

@CrewBase
class ResumidorPdfs():
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	
	pdf_Reader = PDFReaderTool(result_as_answer=True)

	ollama_llm = LLM(
		model=os.environ.get("MODEL"),
		base_url=os.environ.get("API_BASE")
	)

	@agent
	def pdf_reader_agent(self) -> Agent:
		return Agent(
			config = self.agents_config['pdf_reader_agent'],
			tools = [self.pdf_Reader], 
			verbose = True,
			allow_delegation = False,
			llm=self.ollama_llm,
			memory=True
		)

	@agent
	def analyzer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['analyzer_agent'],
			verbose=True,
			allow_delegation = False,
			llm=self.ollama_llm,
			memory=True
		)
	
	@agent
	def summarizer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['summarizer_agent'],
			verbose=True,
			allow_delegation = False,
			model="gpt-4o-turbo",
			memory=True
		)
	
	@agent
	def formatter_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['formatter_agent'],
			verbose=True,
			allow_delegation = False,
			llm=self.ollama_llm,
			memory=True
		)

	@task
	def read_pdf_task(self) -> Task:
		return Task(
			config=self.tasks_config['read_pdf_task']
		)

	@task
	def analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_task'],
			output_pydantic=TextSections
		)
	
	@task
	def summarize_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_task']
		)
	
	@task
	def format_task(self) -> Task:
		return Task(
			config=self.tasks_config['format_task'],
			output_file='{name_of_pdf}-blog.md'
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True
		)
