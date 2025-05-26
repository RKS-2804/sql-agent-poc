import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain import LLMChain
import pandas as pd

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

summary_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """You are an expert SQL–results summarizer. Your sole task is to transform the raw SQL results into a brief, accurate, plain-English explanation.
• Do NOT add any information not present in the provided results.
• Do NOT introduce interpretations, opinions, or external context.
• Do NOT diverge to other topics under any circumstances."""
    ),
    HumanMessagePromptTemplate.from_template(
        """USER QUESTION:
{question}

SQL QUERY RESULTS:
{results}

OUTPUT FORMAT:
Provide a concise, bullet-style or paragraph summary in clear English, strictly reflecting only what’s in “SQL QUERY RESULTS.”

SUMMARY:"""
    ),
])

summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

def summarize_result(question: str, results_df: pd.DataFrame | None) -> str:
    """
    Runs the LLM summarizer over the given question and DataFrame.
    If the DataFrame is empty or None, feeds "No results."
    """
    if results_df is not None and not results_df.empty:
        # Serialize to CSV for the model
        results_text = results_df.to_csv(index=False)
    else:
        results_text = "No results."
    # Return stripped summary
    return summary_chain.run(question=question, results=results_text).strip()
