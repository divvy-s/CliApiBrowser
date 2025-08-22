# Gemini CLI Browser
A simple CLI tool to interact with Google's Gemini models.

Supports switching models, simulating typing effects, and saving AI responses.

## Features
Query Gemini directly from the terminal

Switch between models

Typing animation for responses

Save the last AI reply to a file

## Installation
Clone the repository:

git clone [https://github.com/yourusername/gemini-cli-browser.git](https://github.com/yourusername/gemini-cli-browser.git)
cd gemini-cli-browser

Install dependencies:

pip install -r requirements.txt

Create a .env file and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

## Usage
Run the browser:

python main.py

## Commands
exit or quit – Exit the browser

/model MODEL_NAME – Switch between gemini-1.5-flash and gemini-1.5-pro

/save filename.txt – Save the last AI reply to a file

Example session
>>> What is the capital of France?
Paris is the capital of France.
--------
>>> /save france.txt
Reply saved to france.txt

## Requirements
Python 3.8+

requests

python-dotenv

rich