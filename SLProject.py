import streamlit as st
import os
from openai import OpenAI
import datetime
import json


def save_session():
    if st.session_state.current_session:
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
        }
    if not os.path.exists("session"):
        os.mkdir("session")
    with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
def load_sessions():
    session_list=[]
    if os.path.exists("session"):
        file_list=os.listdir("session")
        for file in file_list:
            if file.endswith(".json"):
                session_list.append(file[:-5:1])
    return session_list
def load_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            with open(f"session/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error("加载失败")
def delete_session(session_name):
    try:
        if os.path.exists(f"session/{session_name}.json"):
            os.remove(f"session/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.messages=[]
                st.session_state.nick_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    except Exception as e:
        st.error("删除失败")
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

st.set_page_config(
    page_title="AI伴侣",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

# page_list=[]

st.title("AI伴侣")

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"
if "nature" not in st.session_state:
    st.session_state.nature="活泼开朗的东北女孩"
#会话表示
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

with st.sidebar:
    st.subheader("AI控制面板")
    if st.button("新建会话",width="stretch"):
       #保存当前会话信息
        save_session()
       #创建新的会话
        if st.session_state.messages:
           st.session_state.messages = []
           st.session_state.current_session = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
           save_session()
           st.rerun()
    st.text("会话历史")
    session_list=load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4,1])
        with col1:
            if st.button(session,width="stretch",key=f"load_{session}",type="primary" if session== st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", icon="🚨",width="stretch",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()
        # st.button(session, width="stretch")
        # st.button("", width="stretch",icon="x")
    st.subheader("伴侣信息")
    #昵称输入框
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name=nick_name
    #性格输入框
    nature = st.text_input("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature=nature
st.text(f"会话名称:{st.session_state.current_session}")
for message in st.session_state.messages:
   st.chat_message(message["role"]).write(message["content"])
sys_prompt="欢迎提问"
user_message=st.chat_input("input something")
if user_message:
    st.chat_message("user").write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})


    #调用dp
    # print([{"role": "user", "content": user_message},*st.session_state.messages])
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": sys_prompt},
            *st.session_state.messages
        ],
        stream=True
    )
    response_message=st.empty()
    full_response=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content=chunk.choices[0].delta.content
            full_response+=content
            response_message.chat_message("assistant").write(full_response)

    # print("大模型返回的结果是：",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content":full_response })
    save_session()
