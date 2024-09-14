from openai import OpenAI


def create_assistant(client, instructions, name=None, model="gpt-4o"):
    assistant = client.beta.assistants.create(
    instructions=instructions,
    name="LLM BOT" if not name else name,
    tools=[{"type": "code_interpreter"}],
    model=model,
    )
    print(f"Assistant succesfully created with {instructions}", assistant)
    return assistant

def delete_assistant(client, assistant):
    return client.beta.assistants.delete(assistant.id)

if __name__ == "__main__":
    client = OpenAI()
    clever_boy = create_assistant(client, "You are a clever boy!")
    not_so_clever_boy = create_assistant(client, "You are not the brightest boy!")
    boys = [clever_boy, not_so_clever_boy]
    for boy in boys:
        deletion = delete_assistant(client, boy)
        print(deletion)
