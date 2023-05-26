import openai
from flask import Flask, request, render_template

app = Flask(__name__)
openai.api_key = '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'

def get_api_response(prompt: str) -> str | None:
    text: str | None = None
    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )
        choices: dict = response.get('choices')[0]
        text = choices.get('text')
    except Exception as e:
        print('ERROR:', e)
    return text

def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)
    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'
    return bot_response

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = get_bot_response(user_input, prompt_list)
        return render_template('index.html', user_input=user_input, bot_response=response)
    return render_template('index.html')

if __name__ == '__main__':
    prompt_list: list[str] = ['You are a Napple_Ai and will answer as a Napple_Ai',
                              '\nHuman: What time is it?',
                              '\nAI: I have no idea, I\'m a Napple_Ai!']
    app.run(debug=True)
