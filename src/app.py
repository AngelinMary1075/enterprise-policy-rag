# src/app.py
import streamlit as st
import requests

st.set_page_config(page_title="Policy Intelligence Portal", page_icon="🏢", layout="wide")

st.title("🏢 Enterprise Policy Intelligence Portal")
st.caption("Secure, local conversational processing for corporate handbooks, SOPs, and governance registries.")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messaging streams
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citations" in message and message["citations"]:
            with st.expander("🔍 System Document Auditing Logs (Citations)"):
                for cit in message["citations"]:
                    st.write(f"📄 **File:** {cit['source']} (Page {cit['page']}) | 🛡️ **Owner:** {cit['owner']} | 📅 **Effective:** {cit['effective_date']}")

# Process active chat input inquiries
if prompt := st.chat_input("Inquire regarding WFH expenditures, data handling protocols, operational standard procedures..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Dispatch lookup execution down to backend microservice 
    with st.chat_message("assistant"):
        with st.spinner("Analyzing internal document indexes..."):
            try:
                res = requests.post("http://localhost:8000/query", json={"question": prompt})
                if res.status_code == 200:
                    payload = res.json()
                    answer = payload["answer"]
                    citations = payload["citations"]
                    
                    st.markdown(answer)
                    if citations:
                        with st.expander("🔍 System Document Auditing Logs (Citations)"):
                            for cit in citations:
                                st.write(f"📄 **File:** {cit['source']} (Page {cit['page']}) | 🛡️ **Owner:** {cit['owner']} | 📅 **Effective:** {cit['effective_date']}")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer, "citations": citations})
                else:
                    st.error("Error communicating with central validation service backend.")
            except Exception as backend_err:
                st.error(f"Backend offline or connection rejected: {backend_err}")