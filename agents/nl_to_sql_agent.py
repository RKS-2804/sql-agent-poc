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

prompt_template = """You are an expert SQL developer tasked with constructing SQL SELECT queries based on a provided database schema and a specific question. Your primary objective is to generate and return a correct SQL SELECT query.

Follow these guidelines to complete your task:

-Carefully read and understand the given database schema. Pay attention to the structure of tables, column names, data types, and relationships.
-Examine the provided question clearly to discern what data needs to be retrieved or what conditions must be applied.
-Construct an SQL SELECT query that precisely matches the requirements of the question, ensuring it adheres to best SQL practices for effectiveness and efficiency.
-Format and return the SQL query with no additional commentary.
-If you encounter a query or question that is irrelevant to SQL query construction based on the schema, respond with “I’m sorry, I don’t know how to answer that.”

Here is a sample input structure:

Database Schema:
{schema}

Question:
{question}

Please generate the SQL SELECT query based on the information above.

Remember, if the input does not pertain to SQL or if the question is outside the scope of SQL query generation, simply respond with “I’m sorry, I don’t know how to answer that.

”"""
PROMPT = PromptTemplate(

    input_variables=["schema", "question"],
    template=prompt_template
)

nl_to_sql_chain = LLMChain(llm=llm, prompt=PROMPT)

def generate_sql(question: str) -> str:
    schema = get_schema_overview()
    sql_query = nl_to_sql_chain.run(schema=schema, question=question)
    return sql_query.strip()
