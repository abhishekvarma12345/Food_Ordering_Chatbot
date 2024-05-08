import ollama
import json

result = "UP"
messages = []
while result == "UP":
    user_msg = input(">> ")
    messages.append({"role":"user", 'content': user_msg})
    stream = ollama.chat(model='foodorderbot', messages=messages,stream=True)

    total_text = []
    each_line = ""
    for chunk in stream:
        cur_chunk = chunk['message']['content']
        if "\n" in cur_chunk:
            total_text.append(each_line + cur_chunk)
            each_line = ""
        else:
            each_line += cur_chunk

        print(cur_chunk, end='', flush=True)
    total_text.append(each_line)

    output_llm1 = "".join(total_text)

    prompt2 = f"""
    customer: {user_msg}
    AI assistant: {output_llm1}
    """
    llm2_messages = [{"role": "user", "content": prompt2}]
    response = ollama.chat(model='endoforder', messages=llm2_messages)
    response = json.loads(response['message']['content'])
    result = response["result"]
    print(f"\nEnd of Order(EOO) or Under Progress(UP)?{result}")
    print()