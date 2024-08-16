import streamlit as st


def main():
    st.set_page_config(page_title='AI DevOps')
    st.title('AI DevOps')

    query_text = st.text_input(
        "What environment do you want to create?",
        key="query",
    )

    if query_text:
        with st.spinner('processing...'):
            handle_user_request(query_text)


def handle_user_request(query):
    pass


if __name__ == '__main__':
    main()
