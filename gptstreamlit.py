import streamlit as st
import os, openai

openai.api_key ="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"

system_msg_default = {'role': 'system', 'content': 'You are GPT, a helpful assistant to a dental receptionist.'}
system_msg_rewrite = {'role': 'system', 'content': 'You are GPT, a helpful assistant to a dental receptionist. You are simply rewriting a draft message for a patient.'}

if "messages" not in st.session_state:
    st.session_state['messages'] = [system_msg_default]
messages = st.session_state['messages']

#display the chat window
st.title("GPT-3 Chat")
st.write("Type your message and press Send to get a response from GPT-3")

#system message:
system_msg = messages[0]
system_msg_input = st.text_input("System message:", value=system_msg['content'], key="system_msg")
if system_msg_input != system_msg['content']:
    system_msg['content'] = system_msg_input
    messages[0] = system_msg
    st.experimental_rerun()

# ask GPT to rewrite what they have in the input box
def toggleMode():
    if system_msg_input == system_msg_default['content']:
        messages[0] = system_msg_rewrite
    else:
        messages[0] = system_msg_default

st.button("Toggle System Msg" , on_click=toggleMode)

# display the messages
for message in messages:
    if message["role"] == "user":
        st.write("User: " + message["content"])
    elif message["role"] == "assistant":
        st.write("Assistant: " + message["content"])

# get user input
user_input = st.text_input("New Msg:", key="user_input")
if user_input != "":
    # make sure its different than the last message
    if user_input != messages[-1]["content"]:
        messages.append({"role": "user", "content": user_input})
        st.experimental_rerun()

## CALLBACKS
def send():
    response=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    st.session_state['user_input'] = ""
    return reply

def clear():
    st.session_state['messages'] = [system_msg]
    st.session_state['user_input'] = ""

# buttons
st.button("Send" , on_click=send)
st.button("Clear" , on_click=clear)
    
# display response
st.write(messages)

# 70 - 90 - 110
    