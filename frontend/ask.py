import json
import requests
import streamlit as st

# App title
st.set_page_config(page_title="💬 GameGuru")

# Select a game input
games = (
    requests.get(url="http://backend:8000/games/list")
    .content.decode("utf-8")[1:-1]
    .split(",")
)
st.session_state.game = st.selectbox(label="Select a game", options=[""] + games)

if st.session_state.game:
    current_game = st.session_state.game
    game_messages = f"{current_game}-messages"

    # Init game state if it does not exist
    if game_messages not in st.session_state.keys():
        st.session_state[game_messages] = [
            {"role": "assistant", "content": f"Ask a question about {current_game}"}
        ]

    # Display game state messages
    for message in st.session_state[game_messages]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User asks a question
    question = st.chat_input(placeholder="Ask a question")

    if question:
        st.session_state[game_messages].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

    # Generate a new response if last message came from the user
    if st.session_state[game_messages][-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                data = {"game": current_game, "user_query": question}
                response = requests.post(
                    url="http://backend:8000/answer", data=json.dumps(data)
                ).content.decode("utf-8")
                # parse response
                response = (
                    response.split("\\n\\n")[0]
                    .strip()
                    .replace('"', "")
                    .replace("\\n", "")
                    .replace("\\", "")
                )
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state[game_messages].append(message)
