questions_and_answers = {
    "what are your hours": "We are open from 9 AM to 6 PM, Monday to Saturday.",
    "how do i book a ticket": "You can book a ticket directly through our website's booking page.",
    "what is your refund policy": "Refunds are processed within 5 to 7 business days.",
    "how do i contact support": "You can reach our support team at support@example.com.",
    "where are you located": "We are located in Bangalore, India."
}

common_words = ["what", "is", "are", "the", "how", "do", "i", "you", "your", "a", "an", "can"]

def find_best_match(user_input):
    user_input = user_input.lower()
    input_words = user_input.split()
    meaningful_input_words = []
    for word in input_words:
        if word not in common_words:
            meaningful_input_words.append(word)

    best_match = None
    highest_score = 0

    for question in questions_and_answers:
        score = 0
        words_in_question = question.split()
        for word in words_in_question:
            if word not in common_words and word in meaningful_input_words:
                score = score + 1

        if score > highest_score:
            highest_score = score
            best_match = question

    if best_match and highest_score > 0:
        return questions_and_answers[best_match]
    else:
        return "Sorry, I do not understand that question. Can you rephrase it?"

print("Chatbot is ready. Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Chatbot: Goodbye!")
        break
    response = find_best_match(user_input)
    print("Chatbot:", response)
