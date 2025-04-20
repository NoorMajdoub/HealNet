
async def flow_injury_full_assessment():
    conversation_history = []
    model = genai.GenerativeModel(MODEL_NAME)

    try:
        print("🩺 Injury Assessment Bot: Let's evaluate your injury.\n")

        # 🌟 Initial dynamic questions
        for _ in range(2):  # You can change this to 3 if you want more questions
            q_prompt = (
                "You're a helpful injury assessment assistant.\n"
                "The user has a bruise or injury and you're trying to evaluate if it could be a fracture.\n"
                f"So far, this is the conversation:\n{''.join(conversation_history)}\n\n"
                "What is the next **different** question you would ask the user to help assess the injury?\n"
                "Ask just one question. Avoid repeating any previous questions."
            )
            q_response = await model.generate_content_async(q_prompt)
            question = q_response.text.strip()

            print(f"Question: {question}")
            user_answer = await get_user_input_async()
            conversation_history.append(f"Q: {question}\nA: {user_answer}\n")

        # 💡 First assessment
        q_final_prompt = (
            "You're a helpful injury assessment assistant.\n"
            f"Based on this conversation:\n{''.join(conversation_history)}\n\n"
            "Do you think the user might be dealing with a fracture? Give a short, clear reasoning."
        )
        q_response = await model.generate_content_async(q_final_prompt)
        response_initial = q_response.text.strip()
        print(f"\n🧠 First diagnosis:\n{response_initial}")

        # 🦴 Physical test suggestion
        q_prompt = (
            "You're a helpful injury assessment assistant.\n"
            "The user has a bruise or injury and you're trying to evaluate if it could be a fracture.\n"
            f"So far, this is the conversation:\n{''.join(conversation_history)}\n\n"
            "What is the physical test you would ask the user to do to confirm if there is a fracture?\n"
            "Ask just one question. Ask the user to evaluate the pain."
        )
        q_response = await model.generate_content_async(q_prompt)
        question = q_response.text.strip()

        print(f"Question: {question}")
        user_answer = await get_user_input_async()
        conversation_history.append(f"Q: {question}\nA: {user_answer}\n")

        # 🧠 Assessment after physical test
        q_final_prompt = (
            "You're a helpful injury assessment assistant.\n"
            f"Based on this updated conversation:\n{''.join(conversation_history)}\n\n"
            "Do you think the user might be dealing with a fracture? Give a short, clear reasoning."
        )
        q_response = await model.generate_content_async(q_final_prompt)
        response_after_test = q_response.text.strip()
        print(f"\n🧠 Updated assessment:\n{response_after_test}")

        # 🏠 Final recommendation
        final_prompt = (
            "You are a medical assistant analyzing the following injury case:\n"
            f"{''.join(conversation_history)}\n\n"
            "Please provide recommendations and home remedies if you think this injury is not dangerous.\n"
            "Otherwise, recommend seeing a doctor."
        )
        q_response = await model.generate_content_async(final_prompt)
        answer = q_response.text.strip()

        print(f"\n✅ Final recommendation:\n{question}")

        conversation_history.append(f"Q: final decision \nA: {answer}\n")

    except Exception as e:
        print(f"❌ Error during assessment: {e}")
        return "⚠️ An error occurred. Please try again or consult a medical professional."


