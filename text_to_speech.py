try:
    from pathlib import Path
    from openai import OpenAI
    import json
except ImportError as e:
    print(f"Error importing modules. Error details: {str(e)}")
    exit(1)

def load_api_key(api_key_file):
    try:
        with open(api_key_file, "r") as json_file:
            data = json.load(json_file)
            return data.get("key")
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding the JSON file. {str(e)}")
        return None

def save_api_key(api_key_file, api_key):
    key = {"key": api_key}
    with open(api_key_file, "w") as json_file:
        json.dump(key, json_file, indent=2)

def text_to_speech(filename, model, voice, text, api_key):
    try:
        client = OpenAI(api_key=api_key)
        file_path = Path(__file__).parent / f"{filename}.mp3"
        
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        response.stream_to_file(file_path)
        print("Audio file created")

    except error.ApiError as e:
        print(f"API Error: {str(e)}")

api_key_file = 'key.json'
api_key = load_api_key(api_key_file)

if api_key is None:
    api_key = input("Enter your API key: ")
    save_api_key(api_key_file, api_key)
    print("API key registered in the file.")
try:
    filename = input("Enter a name for your audio file (without extension): ")
    model = input('Enter a model, for example "tts-1": ')
    voice = input('Enter a voice, for example "alloy": ')
    text = input("Enter the text you want the voice to say: ")

    text_to_speech(filename, model, voice, text, api_key)

except KeyboardInterrupt:
    print("\n process canceled by the user")
