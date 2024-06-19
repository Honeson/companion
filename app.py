import streamlit as st
from main import get_answer
# Custom CSS
def local_css(file_name):
    with open(file_name, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def animated_text(text, animation_class):
    return f'<div class="{animation_class}">{text}</div>'

def display_tips():
    st.sidebar.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <div class="sidebar-tips">
        <details open>
            <summary><h4><i class="fas fa-lightbulb"></i> Tips for an Enriching Conversation</h4></summary>
            <ul class="fa-ul">
                <li><span class="fa-li"><i class="fas fa-heart"></i></span>Be open and honest about your feelings.</li>
                <li><span class="fa-li"><i class="fas fa-sun"></i></span>Share both your joys and your concerns.</li>
                <li><span class="fa-li"><i class="fas fa-book-open"></i></span>Reflect on the verses and how they relate to your life.</li>
                <li><span class="fa-li"><i class="fas fa-dove"></i></span>Take a moment to meditate on the guidance.</li>
                <li><span class="fa-li"><i class="fas fa-comments"></i></span>Feel free to ask follow-up questions.</li>
                <li><span class="fa-li"><i class="fas fa-hand-holding-heart"></i></span>This is a supportive space for your journey.</li>
            </ul>
        </details>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load CSS
    local_css("styles.css")

    

    # Sidebar
    st.sidebar.markdown(animated_text("🙏 SoulVerse 🕊️", "fade-in-text"), unsafe_allow_html=True)
    display_tips()

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'new_conversation' not in st.session_state:
        st.session_state.new_conversation = True
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Custom CSS for labels
    st.markdown("""
    <style>
    .label {
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    # App description
    st.markdown("""
<div class="app-description">
    I am SoulVerse, your companion in faith. 
    I'm here to walk with you through all life's moments, offering personalized Bible verses and insights. Whether you need comfort during challenges, guidance for decisions, or a companion to share your joys, just share your thoughts with me. I'll provide compassionate support with relevant scriptures, helping you find deeper meaning and relief in your journey. 
</div>
""", unsafe_allow_html=True)

    # Religion selection
    #religion = st.selectbox("Select your faith:", ["Christian"], key='religion')

    # Display previous messages
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html=True)

    # User input
    user_input = st.text_area("Share your current situation or concern:", key='user_input')
    

    if st.button("Seek Guidance", key='seek_guidance'):
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Prepare input for get_answer
            if not st.session_state.new_conversation:
                context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                full_input = f"{context}\nUser: {user_input}"
            else:
                full_input = user_input
                st.session_state.new_conversation = False

            # Get response
            response = get_answer(full_input)

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Clear user input using st.session_state
            
            st.experimental_rerun()
            st.session_state.user_input = ""
        else:
            st.warning("Please share your situation before seeking guidance.")

    # Option to clear chat history
    if st.button("Start New Conversation"):
        st.session_state.messages = []
        st.session_state.new_conversation = True
        #st.session_state.user_input = ""
        st.experimental_rerun()

    st.markdown("---")
    st.write("🌐 Connected to: SoulVerse")
    st.caption("Made with ❤️ by Sunny")

if __name__ == "__main__":
    main()
