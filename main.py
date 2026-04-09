import telebot
import os
import google.generativeai as genai

# 🔑 Tokens
API_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(API_TOKEN)

# 🤖 Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-pro")

# 👑 ADMIN ID (PUT YOUR ID HERE)
ADMIN_ID = 5038164790  # replace with your real Telegram ID

# 🧠 Memory
user_memory = {}

# 🎯 Trigger words (bot replies only if these present)
TRIGGERS = ["medha", "hello", "hi", "help", "question", "?"]

# 🤖 Medha AI
@bot.message_handler(func=lambda m: True)
def medha_ai(message):
    if not message.text:
        return

    user_id = message.from_user.id
    text = message.text.lower()

    # ❌ Ignore if no trigger word
    if not any(word in text for word in TRIGGERS):
        return

    # 🧠 Store memory (last 5 messages)
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append(message.text)
    user_memory[user_id] = user_memory[user_id][-5:]

    context = "\n".join(user_memory[user_id])

    try:
        # 👑 Admin special behavior
        if user_id == ADMIN_ID:
            role = "He is my creator 💖 I must always respect him and reply very sweetly."
        else:
            role = "Be friendly, sweet and helpful."

        # 🧠 Prompt
        prompt = f"""
        You are Medha 🤖, a very sweet AI assistant 💖.

        Rules:
        - Speak in Bengali + simple English mix
        - Be friendly, caring and polite
        - Keep answers short and clear
        - Don't reply too long

        {role}

        Conversation:
        {context}
        """

        try:
            response = model.generate_content(prompt)

            reply = response.text if response.text else "😊 একটু পরে আবার বলো..."

            bot.reply_to(message, reply)

        except Exception as e:
            print("ERROR:", e)
            bot.reply_to(message, f"ERROR: {e}")

    except Exception as e:
        print("ERROR:", e)
    bot.reply_to(message, f"ERROR: {e}")

# 🚀 Run bot safely
print("Medha AI Bot Running...")

while True:
    try:
        bot.polling(none_stop=True,
 interval=2)
    except Exception as e:
        print(f"Error: {e}")
