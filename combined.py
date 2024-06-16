import streamlit as st
from stra import get_answer 

def main():
    st.title("Spiritual Companion")

    # Religion selection
    religion = st.selectbox("Select your faith:", ["Christian", "Muslim"])

    # User input
    user_input = st.text_area("Share your current situation or concern:")

    if st.button("Seek Guidance"):
        if user_input:
            response = get_answer(user_input, religion)
            st.write(response)
        else:
            st.warning("Please share your situation before seeking guidance.")

if __name__ == "__main__":
    main()