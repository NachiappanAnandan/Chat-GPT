# import openai
#
# # Set your OpenAI API key
# openai.api_key = 'your-api-key-here'
#
# # Define a function to create a chat completion
# def create_chat_completion(messages):
#     response = openai.ChatCompletion.create(
#         model="gpt-4",  # or "gpt-3.5-turbo", depending on your needs
#         messages=messages,
#         max_tokens=100
#     )
#     return response.choices[0].message['content'].strip()
#
# # Define the conversation history
# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Write a poem about the sea."}
# ]
#
# # Generate and print the chat completion
# output = create_chat_completion(messages)
# print(output)



