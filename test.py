import openai

openai.api_key = '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'
openai.base_url = "https://api.pawan.krd"

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "How do I list all files in a directory using Python?"},
    ],
)

print(completion.choices[0].message.content)