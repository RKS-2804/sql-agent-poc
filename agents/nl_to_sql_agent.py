import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from agents.schema_agent import get_schema_overview

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

prompt_template = """You are an expert SQL developer.
Using this database schema:
{schema}

Write a correct SQL SELECT query to answer:
{question}

Return ONLY the SQL query."""
PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=prompt_template
)

nl_to_sql_chain = LLMChain(llm=llm, prompt=PROMPT)

def generate_sql(question: str) -> str:
    schema = get_schema_overview()
    sql_query = nl_to_sql_chain.run(schema=schema, question=question)
    return sql_query.strip()
