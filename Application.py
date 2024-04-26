import streamlit as st
from st_pages import Page, add_page_title, show_pages


class App:

    def __init__(self):
        show_pages(
            [
                Page('./UI/Chat.py', 'Chatbot PPGSPI', '💬'),
            ]
        )

    def render(self) -> None:
        st.set_page_config(layout='wide')


if __name__ == "__main__":
    App().render()
