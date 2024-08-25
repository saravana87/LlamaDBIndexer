import streamlit as st
from llama_index.core import Settings, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
import logging

# Set up Streamlit page configuration
st.set_page_config(page_title="Chat with RAG Agent", page_icon="💬", layout="centered")

# Set up logging (optional)
# logging.basicConfig(level=logging.DEBUG)

# Initialize settings for the LLM
llm = OpenAI(model="gpt-4", temperature=0)

# Cache the agent initialization to avoid reloading every time the app is run
@st.cache_resource
def initialize_agent():
    # Load indexes and create query engines
    storage_context_2025 = StorageContext.from_defaults(persist_dir="./cdi_2025_index")
    pinson_query_engine_2025 = load_index_from_storage(storage_context_2025, index_id="cdi_2025_01").as_query_engine()

    storage_context_cdi = StorageContext.from_defaults(persist_dir="cdi_data_index")
    cdi_query_engine = load_index_from_storage(storage_context_cdi, index_id="cdiplus_index").as_query_engine()

    storage_context_webinar = StorageContext.from_defaults(persist_dir="webinar_data_index")
    webinar_query_engine = load_index_from_storage(storage_context_webinar, index_id="webinar_index").as_query_engine()

    return agent

# Initialize the agent
agent = initialize_agent()

# Streamlit UI
st.title("Chat with RAG Agent 💬")
st.info("Ask questions about the data!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle user input and generate responses
def handle_input():
    prompt = st.session_state.prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        with st.spinner("Generating response..."):
            response = agent.chat(prompt)
            logging.debug(f"Response object: {response}")
            # Check if response has a message attribute
            if hasattr(response, 'message'):
                content = response.message
            else:
                content = response
            st.session_state.messages.append({"role": "assistant", "content": content})
    except ValueError as e:
        logging.error(f"Error generating response: {e}")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't generate a response. Please try again."})
    # Clear the input field by resetting the session state
    st.session_state.prompt = ""

# Input text box
st.text_input("You: ", key="prompt", on_change=handle_input)

# Display message history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**RAG Agent:** {message['content']}")
