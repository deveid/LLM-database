import streamlit as st
from llm import execute_user_query
# Sample images for dropdown
image_options = {
    "railway": "images/dvdrental.png",
}

response_options = {
        "railway": "Sure! Here’s some information from the dvdrental database.",
        "medicore": "Fetching medical data for you...",
        "finledger": "Accessing financial records...",
    }

# dropdown choices for text response
def query_database(database, question):
    return response_options.get(database, "Sorry, no data available.")

# Divide the page into two equal columns
col1, col2 = st.columns(2)

# Left Side: Image Selection
with col1:
    st.subheader("Database Schema")
    selected_image = st.selectbox("Choose the database to see schema:", list(image_options.keys()))
    st.image(image_options[selected_image], caption=selected_image, use_container_width=True)

# Right Side: Text Input & Dropdown
with col2:

    st.subheader("User Input & Response")
    db_selected_response = st.selectbox("Choose a database:", list(response_options.keys()))

    user_input = st.text_input("Enter question you'd like to ask from the database:")

    if st.button("Submit"):
        if not user_input.strip():
            st.error("Please enter a question before submitting.")
        else:
            with st.spinner("Processing your request..."):
                response = execute_user_query(db_name=db_selected_response, question=str(user_input))
            st.write("### Response Query:", response[0])
            st.write("### Response:", response[1])
            st.success(response[1])
