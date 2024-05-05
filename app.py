## Conversational Q&A ChatBot

## Importing Libraries
import streamlit as st
import os
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chat_models import ChatOpenAI

##Streamlit UI

st.set_page_config(page_title="Conversational Q&A ChatBot", layout="centered")
st.header("Hey, Let's Chat")

from dotenv import load_dotenv
load_dotenv()

chat=ChatOpenAI(openai_api_key=os.getenv("OPEN_API_KEY"),temperature=0.6)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

if 'flowmessages' not in st.session_state:
     st.session_state['flowmessages']=[
          SystemMessage(content="You are a general chatbot which can also educate the user about carbon footprint and calculate their personal carbon footprint if they ask to calculate, be interactive and ask the questions one by one to calculate the carbon footprint. I want you to ask all the carbon footprint calculation questions in detail and i want most accurate answers. Ask the following questions, their geographical location, mode of transport, milage, kilometers of travel, energy consumption, dietry choices, flight travel, if they recycle waste or not.")
          ]
     

# Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()


# Set up sidebar with various options
with st.sidebar.expander(" 🛠️ Settings ", expanded=False):
    # Option to preview memory buffer
    if st.checkbox("Preview memory buffer"):
        st.write(st.session_state.entity_memory.buffer)
    MODEL = st.selectbox(
        label="Model",
        options=[
            "gpt-3.5-turbo",
            "text-davinci-003",
            "text-davinci-002",
            "code-davinci-002",
        ],
    )
    K = st.number_input(
        " (#)Summary of prompts to consider", min_value=3, max_value=1000
    )

# Create a ConversationEntityMemory object if not already created
if "entity_memory" not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=chat, k=K)
     
# Add a button to start a new chat
st.sidebar.button("New Chat", on_click=new_chat, type="primary")


def get_chatmodel_response(question):
     
     st.session_state['flowmessages'].append(HumanMessage(content=question))
     answer=chat(st.session_state['flowmessages'])
     st.session_state['flowmessages'].append(AIMessage(content=answer.content))
     st.session_state.past.append(question)
     st.session_state.generated.append(answer.content)

     return answer.content

input=st.text_input("Input: ", key="input")
response=get_chatmodel_response(input)


# loader = TextLoader('data.txt')
# index = VectorstoreIndexCreator().from_loaders([loader])

# output = index.query(input, llm=ChatOpenAI())

# submit=st.button("Ask the Question")

# if submit:
#      st.subheader("The response is : ")
#      st.write(response)

question1=st.button("What is Carbon Footprint?")

if question1:
     response=get_chatmodel_response("What is Carbon Footprint")

question2=st.button("Calculate my carbon footprint")

if question2:
     response=get_chatmodel_response("Calculate my carbon footprint, ask all the inputs one by one and i shall provide u with the inputs, give the final answer in unit of tons")

question3=st.button("Measures to reduce my carbon footprint")

if question3:
     response=get_chatmodel_response("Give me some measures to reduce my carbon footprint in an interactive and attractive manner")

# Allow to download as well
download_str = []
# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.info(st.session_state["past"][i], icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])


# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label=f"Conversation-Session:{i}"):
        st.write(sublist)

# Allow the user to clear all stored conversation sessions
if st.session_state.stored_session:
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session
