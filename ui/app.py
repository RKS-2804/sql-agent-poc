import os
import sys
import streamlit as st

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.auth import register_user, verify_credentials
from utils.chat_history import fetch_history_from_db, save_message
from agents.nl_to_sql_agent import generate_sql
from agents.sql_executor_agent import run_sql_query
from agents.summarizer_agent import summarize_result

def login():
    st.title("🔐 Login or Register")
    action = st.radio("Select action:", ["Login", "Register"])

    if action == "Register":
        st.subheader("Create a new account")
        u = st.text_input("Username", key="reg_user")
        p = st.text_input("Password", type="password", key="reg_pwd")
        if st.button("Register", key="reg_btn"):
            if register_user(u, p):
                st.success("Registration successful! Now please log in.")
            else:
                st.error("Username taken.")
        st.stop()

    st.subheader("Existing user login")
    u = st.text_input("Username", key="login_user")
    p = st.text_input("Password", type="password", key="login_pwd")
    if st.button("Login", key="login_btn"):
        if verify_credentials(u, p):
            st.session_state.username = u
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")
    if not st.session_state.get("username"):
        st.stop()

def chat_interface():
    st.title("💬 SQL Query Chatbot")
    st.write(f"Hello, **{st.session_state.username}**!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = fetch_history_from_db(st.session_state.username)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["message"])

    q = st.chat_input("Type your question here...")
    if q:
        st.session_state.chat_history.append({"role":"user","message":q})
        with st.chat_message("user"):
            st.markdown(q)
        save_message(st.session_state.username, "user", q)

        sql = generate_sql(q)
        df  = run_sql_query(sql)
        ans = summarize_result(q, df)

        with st.chat_message("assistant"):
            st.markdown(f"**SQL:** `{sql}`")
            if df is not None and not df.empty:
                st.dataframe(df)

                st.subheader("Visualize Results")
                nums = df.select_dtypes("number").columns.tolist()
                if nums:
                    ct = st.selectbox("Chart type", ["Line","Bar","Area"])
                    y  = st.selectbox("Y-axis", nums)
                    x  = st.selectbox("X-axis (optional)", [""]+df.columns.tolist())
                    if st.button("Generate Chart"):
                        cdf = df.set_index(x) if x else df
                        if ct=="Line": st.line_chart(cdf[y])
                        if ct=="Bar":  st.bar_chart (cdf[y])
                        if ct=="Area":st.area_chart(cdf[y])

            st.markdown(f"**Answer:** {ans}")
        save_message(st.session_state.username, "assistant", f"SQL: {sql}\nAnswer: {ans}")

def main():
    if "username" not in st.session_state:
        st.session_state.username = None
    if st.session_state.username is None:
        login()
    else:
        chat_interface()

if __name__ == "__main__":
    main()
