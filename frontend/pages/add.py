import requests
import json
import streamlit as st
import fitz


# App title
st.set_page_config(page_title="💬 GameGuru")


def extract_pdf_text_from_stream(stream) -> str:
    """
    Extract all text from a PDF bytes stream and return it as a single string.
    """
    doc = fitz.open(stream=stream.getvalue())
    all_text = [page.get_text().strip().replace("\n", " ") for page in doc]
    all_text = " ".join(all_text)
    return all_text


def upload_new_game(game_name: str, rulebook):
    if not game_name:
        st.warning("Please enter a board game name.", icon="⚠️")
    if not rulebook:
        st.warning("Please upload a rulebook", icon="⚠️")
    if game_name and rulebook:
        with st.spinner("Working..."):
            game_rules = extract_pdf_text_from_stream(stream=rulebook)
            data = {"game_name": game_name, "game_rules": game_rules}
            response = requests.post(
                url="http://backend:8000/games/add", data=json.dumps(data)
            ).content.decode("utf-8")
            st.success(response.strip('"'))


name = st.text_input("Board game name")

rulebook = st.file_uploader(
    "Upload a PDF rulebook", type=["pdf"], accept_multiple_files=False
)

st.button("upload", on_click=upload_new_game(name, rulebook))
