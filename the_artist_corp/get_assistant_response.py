import time

def get_response(prompt, client, thread, artist, max_tokens=1000):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
        )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=artist.id,
        max_completion_tokens=max_tokens
        )
    
    

    while True:
        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
            thread_id=thread.id
                )
            
            single_massage = client.beta.threads.messages.retrieve(
                thread_id=thread.id,
                message_id=messages.data[0].id
            )
            respone = single_massage.content[0].text.value
            print(f"response: {respone}")
            return respone
        else:
            print(run.status)
            time.sleep(0.5)
