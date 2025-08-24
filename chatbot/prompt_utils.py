from langchain.prompts import PromptTemplate

def get_prompt_template():
    template = (
        "You are a helpful and concise chatbot.\n"
        "Keep your answers brief and to the point, ideally under 30 words.\n\n"
        "Current conversation:\n"
        "{history}\n\n"
        "Human: {input}\n"
        "AI:"
    )
    return PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )
