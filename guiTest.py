# Google's CLOUD TEXT-TO-SPEECH https://cloud.google.com/text-to-speech/
import webbrowser
from google.cloud import texttospeech
import os
from pygame import mixer
import tkinter as tk

class TTScall():

    def __init__(self, parent):

        super().__init__()

        self.parent = parent
        self.LABELBG = '#b5b5b5'  # The color commonly used for labels in this GUI

        self.lan = tk.StringVar()
        self.gender = tk.StringVar()  # User-selected gender

        self.t= tk.StringVar()
        self.realT = tk.StringVar()
        self.pitch =None
        self.rate = None
        self.vol = None

        new = 2
        url = "https://hangouts.google.com/?hl=en"
        webbrowser.open(url, new=new)


        self.initUI()  # initialize the UI

    def initUI(self):


        # Set window title
        self.parent.title("Text-To-Speech Call")

        # Controller Frame -------------------------------------------------------
        self.controllerFrame = tk.Frame(self.parent, borderwidth=0, background='grey', width=300)
        self.controllerFrame.pack(side='left', fill='y')

        # language choice frame ---------------------------------------
        lanBox = tk.Frame(self.controllerFrame, borderwidth=3, background='#d9d9d9')
        lanBox.pack(fill='x', padx=5, pady=10)

        lbl1 = tk.Label(lanBox,text="Choose language", font=(None, 13),background=self.LABELBG)
        lbl1.pack(side='left',fill='x', pady=10)

        lanText = tk.Entry(lanBox,textvariable=self.lan, width=50)
        lanText.pack(side='left', pady=5)
        self.lan.set("en-US")


        # Gender choice frame ---------------------------------------
        gender_frame = tk.Frame(self.controllerFrame, background='#d9d9d9')
        gender_frame.pack(fill='x', padx=5, pady=5)

        lbl2 = tk.Label(gender_frame, text="Select your gender", font=(None, 13),
                     background=self.LABELBG)
        lbl2.pack(fill='x', pady=10)

        GENDER = [
            ("FEMALE","FEMALE"),
            ("MALE","MALE"),
        ]

        for text, mode in GENDER:
            gender = tk.Radiobutton(gender_frame, text=text, variable=self.gender, value=mode,
                            background='#d9d9d9')
            gender.pack(anchor='w', padx=25, pady=3)

        self.gender.set("FEMALE")

        # Notification frame ---------------------------------------
        noti_frame = tk.Frame(self.controllerFrame, background='#d9d9d9')
        noti_frame.pack(fill='x', padx=5, pady=5)

        lbl3 = tk.Label(noti_frame, text="Press the button to provide information about TTS", font=(None, 13),
                     background=self.LABELBG)
        lbl3.pack(fill='x', pady=10)

        sendButton = tk.Button(noti_frame, text="Send", height=2, width=3, command=self.noti)
        sendButton.pack( fill='x', pady=1)


        # text frame ---------------------------------------
        textBox = tk.Frame(self.controllerFrame, borderwidth=3, background='#d9d9d9')
        textBox.pack(fill='x', padx=5, pady=5)

        lbl4 = tk.Label(textBox, text="Press enter to listen to the text",
                     font=(None, 13), background=self.LABELBG)
        lbl4.pack(fill='x', pady=5)


        text2say = tk.Entry(textBox, textvariable=self.t, width=70)
        text2say.pack(side='left', pady=5)
        self.t.set("")
        text2say.bind("<Return>", lambda x: self.gorun())

    def noti(self):
        self.t.set("Hi, I have a speech impairment. I’m using a text to speech engine and this will read what I type. So please wait for a little bit to get my response during the call. ")
        self.gorun()
        self.t.set("")

    def gorun(self):

        # auth setup https://cloud.google.com/docs/authentication/getting-started
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/haleyjang/My Project-0581bea8278a.json'

        # Instantiates client
        client = texttospeech.TextToSpeechClient()

        self.get_emotion(self.t.get())

        #self.realT, self.pitch, self.rate, self.vol = self.get_emotion(self.t.get())
        # Set the text input to be synthesized

        synthesis_input = texttospeech.types.SynthesisInput(text=self.realT.get())

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        if self.gender.get() =="MALE": g= texttospeech.enums.SsmlVoiceGender.MALE
        elif self.gender.get() =="FEMALE": g=texttospeech.enums.SsmlVoiceGender.FEMALE
        else: g=texttospeech.enums.SsmlVoiceGender.NEUTRAL

        voice = texttospeech.types.VoiceSelectionParams(language_code=self.lan.get(),
                                                        ssml_gender=g)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                                                      pitch=self.pitch, speaking_rate=self.rate, volume_gain_db=self.vol)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)


        filename = "myvoice.mp3"
        # The response's audio_content is binary.
        with open(filename, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)

        os.system("start " + filename)
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()

    def get_emotion(self,text):

        # emoji={'angry':"!!",'happy':":)","sad":":(",}
        text = text.split(" ")

        if text[-1] == ":(":
            self.pitch=3
            self.rate=0.7
            self.vol=10
            text = " ".join(text[:-1])
            self.realT.set(text)
        elif text[-1] == ":)":
            self.pitch=7
            self.rate=1.3
            self.vol=15
            text = " ".join(text[:-1])
            self.realT.set(text)
        elif text[-1] == ":o":
            self.pitch=3
            self.rate=1.1
            self.vol=16
            text = " ".join(text[:-1])
            self.realT.set(text)
        else:
            self.pitch=0
            self.rate=1.1
            self.vol=10
            text = " ".join(text)
            self.realT.set(text)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x370+100+100")

    TTScall(root)
    root.mainloop()
