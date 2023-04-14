import openai
from flask import Flask, render_template, request, Markup


app = Flask(__name__)
openai.api_key = "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"


@app.route("/", methods=("GET", "POST"))
def get_story():
    '''
    Give flask the story generated from the generate_story function
    Parameters:
    -----------
    None
    Returns:
    --------
    A html template with the generated story.
    '''
    if request.method == "POST":
        prompt = request.form["prompt"]
        genre = request.form["genre"]
        title, story,history_fact = generate_story(prompt, genre)
        return render_template("index.html", title=title, story=story,history_fact=history_fact)
    else:
        return render_template("index.html", title=None, story=None,history_fact=None)
        

def generate_story(prompt, genre):
    '''
    Prints a summary of the physical therapy plan based on the users inputs.
    Parameters:
    -----------
    promt: str
        The basic story structure, for example, characters, events, time...
    genre: str
        The idea one wants to convery to the kid
    Returns:
    --------
    title: str
        The title of the story
    story: str
        The story conent
    history_fact: str
        an interesting historical fact related to the story
    Returns:
    '''

    # Set up the parameters for generating the story
    model = "text-davinci-003"
    
    # Add genre to the prompt
    prompt_with_genre = f"Generate an exciting story with a title and proper English grammar and punctuations on the topic of {prompt} that can reflect the merits of {genre},"
    
    
    # Generate the title
    title_response = openai.Completion.create(
        engine=model,
        prompt=prompt_with_genre,
        temperature=0.5,
        max_tokens=8,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    # Get the generated title
    title = title_response.choices[0].text.strip()
    
    # Add title to the prompt
    prompt_with_title = f"{prompt_with_genre} {title}."
    
    # Generate the story
    story_response = openai.Completion.create(
        engine=model,
        prompt=prompt_with_title,
        temperature=0.5,
        max_tokens=2500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Get the generated story
    initial_story = story_response.choices[0].text.strip()
    
    
    # Add appropriate paragraphs
    paragraph_length = 5  # Average sentence length for a paragraph
    sentences = initial_story.split('.')
    num_sentences = len(sentences)
    num_paragraphs = int(num_sentences / paragraph_length)
    paragraphs = []
    story = ''
    for i in range(num_paragraphs):
        start_idx = i * paragraph_length
        end_idx = min((i+1) * paragraph_length, num_sentences)
        paragraph = ".".join(sentences[start_idx:end_idx]) + "."
        paragraphs.append(paragraph)

    
   
    story = Markup("<br>".join(paragraphs))

    fact_response = openai.Completion.create(
        engine=model,
        prompt=f"Generate an interesting historical fact about any person or event that appeared in {story} story for kids",
        temperature=0.5,
        max_tokens=2500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )   
    # Get the generated title
    history_fact = fact_response.choices[0].text.strip()

    return  title, story, history_fact
