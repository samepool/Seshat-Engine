This is Seshat, a program that I wrote to help enforce that the creativity of man does not go quietly into the darkness due to the abilities offered by Everyone's desire to flood the market.

What Seshat is intended to be: It is intended to be a writing assistant that compiles characters, data, and events into a world bible.
    -> If writing non-fiction work such as reports it is meant to highlight cited notes and allow the writer to access them for ease of viewing data and context.

What it isn't intended to do: It is not intended to allow the writer to rely on AI to compose a book and claim it as their own. This is meant to be a demonstration for my self, and possibly a product provided to serious writers who wish to exercise artistic expression that technology does not have to be all or nothing, it can be applied to ensure that life is easier but still give full control to the user not the product or product's company.

Stack:
As it deals with data...Python...maybe some Rust thrown in to ensure that the back end is stable and ensures that it works.
Front end...Standard Javascript-HTML-CSS for styling and creating templates and web-pages.

Workflow:

Step 1: Writer Types Idea
    -> Seshat does two things
            1-> It saves the page like a word document (using Markdown)
            2-> The Key (Breaks down the Who, What, Where, Why, and What is the Significance)
                            (Visual: Mark walked down Briton Beach towards Lefton
                                Entry examples.
                                    Character: Mark was walking down Briton Beach towards Lefton
                                    Places: 1 - Briton Beach - a Beach
                                            2 - Lefton - A town at the end of Briton Beach
                                    Entry 2: Mark met Sheri in Lefton town square where a guard was stationed
                                            Character: Mark walked down Briton Beach and met Sheri in Lefton
                                                       Sheri met Mark in Lefton Square
                                            Places: Briton Beach - A Beach that led to Lefton
                                                    Lefton - a town with a square and a guard
                            )
As you can see the entries are meant to get more complex as the writing continues. That way if you are writing a story or paper you can look at this and see what your plot line for the character has been thus far.

Requirements for the project:
 fastapi - In the context of Seshat, think of FastAPI as the central nervous system of your application. It is a modern, high-performance web framework for Python that allows the "Frontend" (where you type) to talk to the "Backend" (where the logic and files live).

Here is why it fits your specific requirements for a lightweight, stable, and user-controlled writing assistant:

1. The "Fast" in FastAPI
It is one of the fastest Python frameworks available, comparable to Node.js and Go. This ensures that as you type, the "Light AI" and file-saving operations happen instantly without lagging your writing experience.

2. Automatic Data Validation (Pydantic)
FastAPI uses Python Type Hints. If you tell it that a "Character" must have a name (string) and an age (integer), FastAPI will automatically catch errors if the data is malformed.

Why this matters for Seshat: It ensures your "World Bible" data stays clean and organized without you writing hundreds of lines of "check" code.

3. Interactive Documentation (Swagger UI)
One of its "superpowers" is that it builds a website for your API automatically.

Once your server is running, you can go to http://127.0.0.1:8000/docs.

You will see a visual interface where you can test your "Save" and "Extract" functions manually without even opening a browser.

4. Asynchronous Support (async/await)
Writing can be a long process. FastAPI is "asynchronous," meaning it can handle saving your file in the background while simultaneously running the AI logic to find "Mark" and "Briton Beach," all without freezing the user interface.


 "uvicorn[standard]"
 pip install uvicorn gives you the basic server, adding the [standard] extra is like upgrading from a standard engine to a turbocharged one.In Python, many libraries have "extra" features that aren't installed by default to keep the initial download small. For Seshat, uvicorn[standard] installs several high-performance C-based libraries that make your backend significantly faster and more robust.
 
 What [standard] adds to your project:
 
 uvloop: This is a drop-in replacement for Python's standard "event loop." It is written in Cython and makes Python's asynchronous networking 2–4 times faster. It's the secret sauce that makes FastAPI's performance comparable to Node.js and Go.
 
 httptools: A lightning-fast, low-level HTTP parser (originally from the Node.js project). It helps Seshat read and understand the "packets" of text you send from your frontend much quicker.
 
 watchfiles: This enables the --reload feature we've been using. It efficiently "watches" your folders for code changes and restarts the server instantly so you don't have to do it manually every time you save a file.
 
 python-dotenv: This allows Seshat to read configuration (like API keys for later AI integration) from a hidden .env file, keeping your secrets safe.
 
 Why this matters for Seshat:
 Since you want Seshat to be a "Writing Assistant," you don't want the program to stutter or lag while you're in a creative flow. The [standard] install ensures that the bridge between your typing and the "World Bible" extraction logic is as near-instant as possible.
 
 A Small Heads-up (Windows Users)
 If you are on Windows, uvloop (the speed booster) is technically not supported, so Uvicorn will automatically fall back to the standard Python loop. Don't worry—the rest of the features still work, and for a writing app, it will still be plenty fast!


  spacy 
  SpaCy is the "brain" of your Seshat project. While FastAPI is the nervous system, SpaCy is the part that actually reads and understands the English language to build your World Bible.
  
  In professional coding, SpaCy is known as an Industrial-Strength Natural Language Processing (NLP) library. It doesn't just "guess" what words mean; it uses a pre-trained statistical model to look at the structure of your sentences.
  
  How SpaCy works for "The Key"
  When you write: "Mark walked down Briton Beach towards Lefton," SpaCy performs several tasks simultaneously:
  Tokenization: It breaks the sentence into individual pieces (Mark, walked, down, Briton, Beach...).
  Part-of-Speech Tagging: It identifies that "Mark" is a Noun and "walked" is a Verb.
    Named Entity Recognition (NER): This is the "magic" for your project.It categorizes specific words:
    Mark $\rightarrow$ PERSON
    Briton Beach $\rightarrow$ LOC (Location) or FAC (Facility)
    Lefton $\rightarrow$ GPE (Geopolitical Entity/Town)

Why we chose SpaCy for Seshat
    Speed: Unlike heavy Large Language Models (LLMs) that require a massive GPU, SpaCy is written in highly optimized Cython. It can process thousands of words per second on a standard laptop.
    
    Consistency: It provides predictable labels. If you write "Mark" ten times, it will consistently identify him as a person, allowing you to compile his timeline accurately.
    
    Privacy: Because SpaCy runs locally on your machine (using that en_core_web_sm model we downloaded), your creative writing never leaves your computer. This aligns perfectly with your goal of keeping the user in control.


  python-multipart
  To round out our "Nervous System" (FastAPI), python-multipart is the specialized translator that allows your backend to understand complex data sent from a web browser.

While we've been talking about sending "text," in a real-world writing app, you often send data in different formats—especially if you eventually want to upload a cover image, a PDF reference, or a large batch of manuscript files at once.

What python-multipart does for Seshat:
Form Data Parsing: Standard HTML <form> elements (the kind used in websites for decades) send data in a specific format called multipart/form-data. FastAPI requires this library to "unwrap" that package and turn it into a Python dictionary you can use.

File Uploads: If you ever want to drag and drop an existing document into Seshat to "Import" it, python-multipart is the engine that handles the streaming of that file onto your hard drive without crashing your RAM.

Security: It helps prevent "denial of service" attacks by safely limiting how much data a user can send at once, ensuring your backend stays stable as per your requirements.

Summary of our Stack
We have officially established the Foundational Four:

FastAPI: The Nervous System (Handles requests).

Uvicorn[standard]: The Turbocharged Engine (Runs the server).

SpaCy: The Brain (Reads and understands your story).

Python-multipart: The Translator (Handles complex data/file inputs).