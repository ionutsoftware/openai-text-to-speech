try:
    from pathlib import Path
    from openai import OpenAI
    import wx
    import json
except ImportError as e:
    show_info(None, f"Error importing modules. Error details: {str(e)}")
    exit(1)

app = wx.App()
app.MainLoop()

def load_api_key(api_key_file):
    try:
        with open(api_key_file, "r") as json_file:
            data = json.load(json_file)
            return data.get("key")
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        show_info(None, f"Error decoding the JSON file. {str(e)}")
        return None

def save_api_key(api_key_file, api_key):
    key = {"key": api_key}
    with open(api_key_file, "w") as json_file:
        json.dump(key, json_file, indent=2)

def ask(parent=None, message='', default_value='', multiline=False):
    result = default_value

    try:
        if multiline:
            dlg = wx.Dialog(parent, title=message)
            sizer = wx.BoxSizer(wx.VERTICAL)
            text_ctrl = wx.TextCtrl(dlg, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, value=default_value)
            sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

            btn_ok = wx.Button(dlg, wx.ID_OK, label="OK")
            btn_cancel = wx.Button(dlg, wx.ID_CANCEL, label="Cancel")
            btn_sizer = wx.StdDialogButtonSizer()
            btn_sizer.AddButton(btn_ok)
            btn_sizer.AddButton(btn_cancel)
            btn_sizer.Realize()

            sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
            dlg.SetSizer(sizer)

            if dlg.ShowModal() == wx.ID_OK:
                result = text_ctrl.GetValue()

        else:
            dlg = wx.TextEntryDialog(parent, message, value=default_value)

            if dlg.ShowModal() == wx.ID_OK:
                result = dlg.GetValue()

    finally:
        dlg.Destroy()

    return result

def show_info(parent, message):
    try:
        dlg = wx.MessageDialog(parent, message, "Information", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
    except wx.PyNoAppError:
        pass
    finally:
        dlg.Destroy()


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
    api_key = ask(parent=None, message="Enter your API key:", default_value="", multiline=False)
    save_api_key(api_key_file, api_key)
    show_info(None, "The API key has been registered in the key.json file")

filename = ask(parent=None, message="Enter a name for your audio file (without extension):", default_value="", multiline=False)
model = ask(parent=None, message='Enter a model to use, for example "tts-1":', default_value="tts-1", multiline=False)
voice = ask(parent=None, message='Enter a voice to use for converting your text. By default, the voice is "alloy":', default_value="alloy", multiline=False)
text = ask(parent=None, message="Enter the text you want the voice to say:", default_value="", multiline=True)

text_to_speech(filename, model, voice, text, api_key)

show_info(None, f"The file has been correctly created. returned from the api: {response}")

