import streamlit as st
import ollama
import json

# Define the menu
menu = """
The restaurant menu has the following categories and items:

1. Antipasti:
    - Bruschetta: €5.00 per piece
    - Caprese Salad: €7.00 per plate

2. Primi:
    - Spaghetti Carbonara: €10.00 per plate
    - Lasagna: €12.00 per plate

3. Secondi:
    - Osso Buco: €15.00 per plate
    - Chicken Piccata: €13.00 per plate

4. Dolci:
    - Tiramisu: €6.00 per piece
    - Cannoli: €5.00 per piece
"""


st.title("Restaurant Food Ordering Chatbot")
# Display the menu in the sidebar
st.sidebar.markdown(menu)

# Initialize variables
result = "UP"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Order something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = ollama.chat(model='foodorderbot', messages=st.session_state.messages,stream=True)
        total_text = []
        each_line = ""
        for chunk in stream:
            cur_chunk = chunk['message']['content']
            if "\n" in cur_chunk:
                total_text.append(each_line + cur_chunk)
                st.write(total_text[-1])
                each_line = ""
            else:
                each_line += cur_chunk
        total_text.append(each_line)
        st.write(total_text[-1])
    
    st.session_state.messages.append({"role": "assistant", "content": "".join(total_text)})
    
    prompt2 = f"""
    customer: {prompt}
    AI assistant: {total_text}
    """
    llm2_messages = [{"role": "user", "content": prompt2}]
    response = ollama.chat(model='endoforder', messages=llm2_messages)
    res = json.loads(response['message']['content'])
    if res["result"] == "EOO":
        st.session_state.messages = []
        with st.chat_message("ai"):
            st.markdown("--- End of Order---")
        