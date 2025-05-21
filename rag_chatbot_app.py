import streamlit as st
from rag_pipeline import build_qa_chain

# Load your QA chain
qa_chain = build_qa_chain()

# Set up Streamlit page
st.set_page_config(page_title="RAG Chatbot", page_icon="📚")
st.markdown("<h1 style='text-align: center;'>RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask me anything based on what I know!</p>", unsafe_allow_html=True)
st.markdown("---")

# Input from user
question = st.text_input("Your question here:")

# Logic to handle answer
if question:
    with st.spinner("Thinking..."):
        result = qa_chain.invoke({"query": question})
        answer = result["result"]

        st.markdown("### Answer")
        if answer.strip().lower() == "unanswerable":
            st.warning("I'm sorry, this question is beyond my expertise based on the information I have.")
        else:
            st.success(answer)

            # Show sources
            st.markdown("### Retrieved Source Documents")
            for i, doc in enumerate(result["source_documents"], 1):
                st.markdown(f"**Source {i}: {doc.metadata.get('title', 'Unknown')} — {doc.metadata.get('section', '')}**")
                st.code(doc.page_content[:300] + "...", language="markdown")
else:
    st.info("Enter a question above to begin!")

