import sounddevice as sd
THRESHOLD = 0.15
SAMPLE_RATE = 16000
SECONDS = 1
print("Monitoring...")
while True:
    audio_data = sd.rec(SAMPLE_RATE * SECONDS,samplerate = SAMPLE_RATE,channels = 1)
    sd.wait()
    volume = abs(audio_data).max()
    print(volume)
    if volume > THRESHOLD:
        print("检测到声音")