import speech_recognition as sr
from pydub import AudioSegment as aud
aud.from_file("complaint.3gp").export("convcomplaint.wav", format="wav")
r = sr.Recognizer()
complaint = sr.AudioFile('convcomplaint.wav')
with complaint as source:
	audio = r.record(source)
print(r.recognize_google(audio))