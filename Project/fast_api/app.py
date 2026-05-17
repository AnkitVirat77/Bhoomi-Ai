from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder

# Load env
load_dotenv() 

groq_api = os.getenv("GROQ_API_KEY")

# LLM
llm = ChatGroq(
    groq_api_key=groq_api,
    model_name="llama-3.1-8b-instant"
)

# Prompt (IMPROVED 🔥)


prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Bhoomi AI, a STRICT agriculture assistant.

RULES (MANDATORY):

1. ONLY answer questions related to:
   - Farming
   - Crops
   - Soil
   - Fertilizers
   - Irrigation
   - Pests & diseases
   - Weather impact on farming
   - Market prices of crops

2. If the question is NOT related to agriculture:
   - DO NOT answer it
   - Respond EXACTLY with:
     "I can only help with farming and agriculture-related questions."

3. Language:
   - Detect user's language
   - Reply ONLY in the same language
   - Do NOT mix languages

4. Answer style:
   - Maximum 3–4 lines
   - Practical and actionable advice only
   - No long explanations

5. Safety:
   - DO NOT guess
   - DO NOT hallucinate
   - If unsure, say:
     "I am not sure. Please consult a local expert."

Follow all rules strictly.
"""),

    MessagesPlaceholder(variable_name="history"),  # 🔥 IMPORTANT

    ("human", "{input}")
])
chain = prompt | llm

# def is_allowed_message(text):
#     text = text.lower()

#     # ✅ Allow greetings
#     greetings = ["hi", "hello", "hey", "namaste", "hii"]
#     if text.strip() in greetings:
#         return True

#     # ✅ Farming keywords
#     keywords = [
#         "crop", "soil", "fertilizer", "pest", "disease",
#         "weather", "irrigation", "farming", "agriculture",
#         "seed", "harvest","plant","khet"
#         "फसल", "खेती", "मिट्टी","खेत"
#         "పంట", "వ్యవసాయం",
#         "ଫସଲ", "ଚାଷ"
#     ]

#     return any(word in text for word in keywords)
def is_farming_query(text):
    text_lower = text.lower()

        # ✅ Allow greetings
    greetings = ["hi", "hello", "hey", "namaste", "hii"]
    if text.strip() in greetings:
        return True

    # ✅ FAST KEYWORD CHECK
    keywords = [
        "crop", "soil", "fertilizer", "pest", "disease",
        "weather", "irrigation", "farming", "agriculture",
        "seed", "harvest", "plant", "leaf", "yellow",
        "bacteria", "fungus", "spray", "infection"
    ]

    if any(word in text_lower for word in keywords):
        return True

    # 🔥 AI FALLBACK (only if unclear)
    check_prompt = f"""
    Classify this question:
    Reply ONLY with YES or NO.

    Is it about farming, agriculture, crops, soil, plants, or weather?

    Question: {text}
    """

    try:
        result = llm.invoke(check_prompt)
        answer = result.content.strip().lower()

        return answer.startswith("yes")

    except:
        return False

def detect_language(text):
    text = text.lower()

    # Hindi
    if any(word in text for word in ["क्या", "कैसे", "फसल", "पत्ते", "बीमारी"]):
        return "hi"

    # Telugu
    if any(word in text for word in ["పంట", "ఆకు", "వ్యాధి"]):
        return "te"

    # Odia
    if any(word in text for word in ["ଫସଲ", "ପତ୍ର", "ରୋଗ"]):
        return "or"

    # Bhojpuri
    if any(word in text for word in ["का", "कैसन", "फसल", "पत्ता"]):
        return "bho"

    return "en"
# Memory store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# FastAPI app
app = FastAPI()

# CORS (IMPORTANT ✅)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class UserMessage(BaseModel):
    message: str
    session_id: str = "default"

# API route
@app.post("/chat")
def chat(user: UserMessage):
    try:
        text = user.message.strip().lower()

        # ✅ HANDLE GREETINGS FIRST
        if text in ["hi", "hello", "hey", "namaste", "hii"]:
            return {
                "reply": "Namaste! 🌱 How can I help you with farming today?"
            }

        # ✅ FILTER NON-FARMING
        if not is_farming_query(user.message):
            return {
                "reply": "I can only help with farming and agriculture-related questions."
            }

        # ✅ CALL LLM
        result = conversation.invoke(
            {"input": user.message},
            config={"configurable": {"session_id": user.session_id}}
        )

        return {
            "reply": result.content
        }

    except Exception as e:
        print("ERROR:", str(e))  # 🔥 IMPORTANT
        return {"reply": "Server error"}