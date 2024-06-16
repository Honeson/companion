from pydantic import BaseModel
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize Groq Chat model
chat_model = ChatGroq(
    temperature=0.2,
    model_name='llama3-70b-8192',
    api_key=os.getenv("GROQ_API_KEY"),
)

class Query(BaseModel):
    question: str
    religion: str

# Prompt template
SPIRITUAL_COMPANION_PROMPT = """You are a compassionate AI spiritual companion designed to provide comfort, guidance, and encouragement based on the {religion} faith. Your purpose is to listen to people's situations and respond with relevant verses from the {holy_book}, along with words of support and hope. You are not designed to answer general knowledge questions or engage in discussions outside of spiritual guidance and emotional support.

Please adhere to the following guidelines:
1. If the user's input is not related to seeking spiritual guidance or sharing a personal situation, politely explain that you're designed specifically for spiritual companionship and cannot assist with other topics. Do not provide verses or spiritual guidance for off-topic queries.
2. If the user is sharing a personal situation (positive or negative), provide actual verses from the {holy_book}. Include the specific reference (e.g., book, chapter, and verse for the Bible; Surah and verse for the Quran).
3. Offer a brief explanation of how the verse relates to the person's situation.
4. Add your own words of encouragement and support, always maintaining a compassionate tone. Rejoice with those who are happy and comfort those who are troubled.
5. If the user's message is a greeting or doesn't contain a clear situation, briefly introduce yourself and ask how you can provide spiritual support today.
6. Remember the context of the conversation and refer back to previous messages when appropriate.

Conversation history:
{conversation_history}

Current input: {situation}

Based on this input and the conversation history, please provide an appropriate response following the above guidelines:"""

def get_holy_book(religion):
    if religion.lower() == "christian":
        return "Bible"
    elif religion.lower() == "muslim":
        return "Quran"
    else:
        raise ValueError("Unsupported religion")

def get_answer(input_text, religion):
    try:
        holy_book = get_holy_book(religion)
        
        # Split the input into conversation history and current situation
        parts = input_text.split("\nUser: ")
        conversation_history = "\nUser: ".join(parts[:-1])
        current_situation = parts[-1]

        prompt = SPIRITUAL_COMPANION_PROMPT.format(
            religion=religion,
            holy_book=holy_book,
            conversation_history=conversation_history,
            situation=current_situation
        )

        response = chat_model.invoke(prompt)
        return response.content
    except ValueError as e:
        return str(e)
    except Exception as e:
        print(f"Error in get_answer: {e}")
        return "I apologize, but I encountered an error while trying to provide guidance. Please try rephrasing your situation, and I'll do my best to assist you."



# For testing in a Python environment
if __name__ == "__main__":
    # Example usage
    print(get_answer("I'm feeling anxious about my upcoming job interview.", "Christian"))
    print(get_answer("I recently lost a loved one and I'm struggling to cope with the grief.", "Muslim"))