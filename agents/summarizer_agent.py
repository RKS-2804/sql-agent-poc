import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
import pandas as pd

load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

summary_prompt = PromptTemplate(
    input_variables=["question", "results"],
    template=(
        "User asked: {question}\n"
        "Here are the SQL results:\n{results}\n"
        "Provide a concise, plain-English summary."
    )
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

def summarize_result(question: str, results_df: pd.DataFrame | None) -> str:
    if results_df is not None and not results_df.empty:
        text = results_df.to_csv(index=False)
    else:
        text = "No results."
    return summary_chain.run(question=question, results=text).strip()
