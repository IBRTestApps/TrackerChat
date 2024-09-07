import streamlit as st
import streamlit_authenticator as st_auth
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain.tools.retriever import create_retriever_tool
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain_core.prompts.prompt import PromptTemplate
from langchain.callbacks import StreamlitCallbackHandler
from os import getenv

pinecone_api_key = getenv('PINECONE_API_KEY')
openai_api_key = getenv('OPENAI_API_KEY')
openai_org_id = getenv('OPENAI_ORG_ID')
index_name = getenv('PINECONE_INDEX')

model = ChatOpenAI(model='gpt-4o', temperature=0.2, max_tokens=1024,
                   api_key=openai_api_key,
                   organization=openai_org_id)
embeddings = OpenAIEmbeddings(model='text-embedding-3-large', api_key=openai_api_key,
                              openai_organization=openai_org_id,
                              dimensions=1024)

template = "Text: {page_content}\n\nmetadata: {URL}"
document_prompt = PromptTemplate.from_template(template)
vectorstore = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
pinecone_retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
pinecone_retriever_tool = create_retriever_tool(pinecone_retriever,
                                                name="Pinecone Vector Database",
                                                description='Find relevant text fragments in a database containing'
                                                            ' legal publications. Use these fragments as context'
                                                            ' for answering questions. The fragments have both text'
                                                            ' and a URL source.',
                                                document_prompt=document_prompt,
                                                document_separator='\n---------------\n')

tools = [pinecone_retriever_tool]

react_template = """Answer the following questions as best you can. 
You have access to the following tools to help you answer the question:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action. You should NOT rewrite the user's question.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question. Try to be as detailed as possible in your answer. Include the URLs in the metadata of the specific text fragments you used to answer the user question. Respond in Dutch.

Begin!
chat history so far {chat_history}
user question: {input}
{agent_scratchpad}
"""
react_prompt = PromptTemplate.from_template(react_template)
react_agent = create_react_agent(llm=model, tools=tools, prompt=react_prompt)
react_parser = ReActSingleInputOutputParser()
react_agent_executor = AgentExecutor(agent=react_agent, tools=tools, max_iterations=3)

# Initialisatie streamlit authenticator
authenticator = st_auth.Authenticate(
    st.secrets["credentials"].to_dict(),
    st.secrets["cookie"]["name"],
    st.secrets["cookie"]["key"],
    st.secrets["cookie"]["expiry_days"],
    st.secrets["preauthorized"])

if st.session_state["authentication_status"] is None:
    st.switch_page('Login.py')
if st.session_state["authentication_status"]:
    authenticator.logout(location='sidebar')

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


st.title('IBR TrackerChat')
if 'name' in st.session_state and st.session_state['name'] is not None:
    st.header(f'Welkom, {st.session_state["name"].split()[0]}')
st.markdown('IBR TrackerChat is een testapplicatie voor een AI aanvulling op de IBR Tracker database van het Instituut'
            ' voor Bouwrecht. Stel hieronder een vraag over de inhoud van de Tracker, en de chatbot zal proberen uw '
            ' vraag te beantwoorden.'
            ' LET OP: De applicatie bevat in de huidige situatie slechts een deel van alle publicaties in de Tracker.'
            ' Zie de info-pagina voor meer details.')
st.divider()
if st.button(label='wis chatgeschiedenis', key='grote_rode_knop', help='verwijder uw chatgeschiedenis: Let op, het taal'
                                                                       'model beantwoord uw volgende vraag dan met een'
                                                                       'blanco gespreksgeschiedenis',
             type='primary'):
    st.session_state['chat_history'] = []

for message in st.session_state['chat_history']:
    with st.chat_message(message.type):
        st.markdown(message.content)

if prompt := st.chat_input(placeholder='Stel uw vraag', key='user_input'):
    with st.chat_message('Human'):
        st.markdown(prompt)
    st.session_state['chat_history'].append(HumanMessage(content=prompt))
    with st.chat_message('AI'):
        st_callback = StreamlitCallbackHandler(st.container())
        response = react_agent_executor.invoke({'chat_history': st.session_state['chat_history'],
                                                'input': prompt}, {'callbacks': [st_callback]})
        st.markdown(response['output'])
    st.session_state['chat_history'].append(AIMessage(content=response['output']))
