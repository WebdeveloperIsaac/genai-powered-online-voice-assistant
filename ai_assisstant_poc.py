import pyaudio
import wave
import requests
import os
import audioOutputTest
from kafka import KafkaConsumer

DEEPGRAM_API_KEY = ""
COHERE_API_KEY = ""

# Headers for API requests
deepgram_headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "audio/wav",
}

cohere_headers = {
    "Authorization": f"Bearer {COHERE_API_KEY}",
    "Content-Type": "application/json",
}
try:
    consumer = KafkaConsumer(
        'streamingsource',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    print("Kafka consumer connected successfully.")
except Exception as e:
    print(f"Error connecting Kafka consumer: {e}")
    
def fetch_all_entries():
    print("Fetched Data From Kafka Topic...")
    all_messages = []
    try:
        for message in consumer:
            data = message.value.decode('utf-8')
            if str(data).__contains__("engine_rpm"):
                all_messages.append(data)
                break
            
    except Exception as e:
        print(f"Error fetching data from Kafka: {e}")

    return all_messages

# Record audio from microphone and save to WAV file
def record_audio(file_path="input_voice.wav", record_seconds=5, sample_rate=16000):
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono
    rate = sample_rate  # Sample rate
    
    p = pyaudio.PyAudio()

    print("Recording...")
    stream = p.open(format=format, channels=channels,
                    rate=rate, input=True,
                    frames_per_buffer=chunk)

    frames = []

    # Record for the specified duration
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Deepgram STT API function
def deepgram_stt(audio_path):
    url = "https://api.deepgram.com/v1/listen?model=nova-2"
    with open(audio_path, 'rb') as audio:
        try:
            response = requests.post(url, headers=deepgram_headers, data=audio, verify=False)
            response.raise_for_status()
            data = response.json()
            return data['results']['channels'][0]['alternatives'][0]['transcript']
        except Exception as e:
            print(f"Error in Deepgram STT: {e}")
            return None

# Cohere LLM API function
def cohere_generate(prompt):
    url = "https://api.cohere.ai/generate"
    payload = {
        # "model": "command-xlarge-nightly",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=cohere_headers, json=payload, verify=False)
        data = response.json()
        return data.get('text', '').strip()
    except Exception as e:
        print(f"Error in Cohere LLM generation: {e}")
        return None

# Main loop for the conversation
def main_loop():
    while True:
        try:
            audio_file = "input_voice.wav"
            record_audio(file_path=audio_file, record_seconds=5)
            print("Processing audio for STT...")
            user_input = deepgram_stt(audio_file)
            if user_input:
                print(f"User said: {user_input}")
            else:
                print("Failed to get text from audio.")
                break
            prompt = """You are an AI car assistant that helps drivers with real-time vehicle information. Respond to user isaac queries about the car’s performance and status. If the user asks for data that’s not yet available & several integrations are on way, politely inform them that the feature is in development.Remember try and give brief & direct answers . Now what ever starts with user is from the user always give an understandable reply these are the current real-time information available for you""" + fetch_all_entries()[0]
            # Step 3: Generate response using Cohere
            prompt += f"User: {user_input}\nAssistant:"
            print("Generating response using Cohere...")
            if str(prompt).lower().__contains__("end conversation"):
                print("Ending conversation...")
                return
            assistant_response = cohere_generate(prompt)
            if assistant_response:
                print(f"Assistant: {assistant_response}")
            else:
                print("Failed to generate response.")
                break

            # Optional: Add TTS for responding with synthesized audio
            print("Generating speech response...")
            audioOutputTest.deepgram_tts(assistant_response)
            tts_audio_path = "output_voice.mp3"
            if os.path.exists(tts_audio_path):
                audioOutputTest.play_audio(tts_audio_path) 

        except Exception as e:
            print(f"Error during the main loop: {e}")
            break

if __name__ == "__main__":
    main_loop()
