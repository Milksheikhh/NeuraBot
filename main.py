import cv2
import speech_recognition as sr
import base64
import time
from groq import Groq
from together import Together
import os
import re
import yt_dlp
import asyncio
from youtubesearchpython import VideosSearch
import vlc
import python_weather
import datetime
from pydub import AudioSegment
from gtts import gTTS
import bot_movement as bot
import time
import playsound3

FFMPEG_DIR = r"C:\PATH_Programs"
os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ["PATH"]
instance = vlc.Instance()
os.environ["GROQ_API_KEY"] = "your_groq_api_key"
os.environ["TOGETHER_API_KEY"] = "your_togetherai_api_key"

weather_client = None

is_music_playing = False
is_tts_speaking = False
stop_tts_flag = False

async def get_weather_client():
    global weather_client
    if weather_client is None:
        weather_client = python_weather.Client(unit=python_weather.METRIC)
    return weather_client

async def cached_weather():
    try:
        client = await get_weather_client()
        weather = await client.get('Euless')
        return {
            "temperature": str(weather.temperature),
            "description": weather.description,
            "humidity": str(weather.humidity),
            "wind_speed": str(weather.wind_speed),
            "feels_like": str(getattr(weather, 'feels_like', 'unavailable')),
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return {
            "temperature": "unavailable",
            "description": "unavailable",
            "humidity": "unavailable",
            "wind_speed": "unavailable",
            "feels_like": "unavailable",
        }

def is_datetime_query(prompt):
    prompt_lower = prompt.lower()
    time_keywords = ['time', 'what time', 'current time']
    date_keywords = ['date', 'what is today', 'what\'s today']
    day_keywords = ['day', 'what day']
    if any(keyword in prompt_lower for keyword in time_keywords):
        return "time"
    elif any(keyword in prompt_lower for keyword in date_keywords) and not is_weather_query(prompt):
        return "date"
    elif any(keyword in prompt_lower for keyword in day_keywords):
        return "day"
    return None

def get_datetime_info(request_type):
    now = datetime.datetime.now()
    if request_type == "date":
        return f"It's {now.strftime('%B %d, %Y')}"
    elif request_type == "time":
        return f"It's {now.strftime('%I:%M %p')}"
    elif request_type == "day":
        return f"Today is {now.strftime('%A')}"
    else:
        return f"{now.strftime('%A')}, the {now.strftime('%d')}{'th' if now.day not in [11,12,13] else 'st' if now.day % 10 == 1 else 'nd' if now.day % 10 == 2 else 'rd' if now.day % 10 == 3 else 'th'} of {now.strftime('%B')} at {now.strftime('%I:%M %p')}"

async def getweather():
    try:
        return await cached_weather()
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return {
            "temperature": "unavailable",
            "description": "unavailable",
            "humidity": "unavailable",
            "wind_speed": "unavailable",
            "feels_like": "unavailable",
        }

def is_weather_query(prompt):
    weather_keywords = ['weather', 'temperature', 'forecast']
    return any(keyword in prompt.lower() for keyword in weather_keywords)

def is_color_query(prompt):
    prompt_lower = prompt.lower()
    color_keywords = ['what color is this', 'what color is my', 'what color is that', 'what color is the']
    general_keywords = ['sky', 'leaves', 'wood', 'grass', 'water', 'fire', 'sun', 'moon']
    if any(keyword in prompt_lower for keyword in color_keywords):
        if not any(keyword in prompt_lower for keyword in general_keywords):
            return True
    return False

class MusicPlayer:
    def __init__(self):
        self.current_player = None
        self.is_playing = False

    def stop(self):
        if self.is_playing and self.current_player:
            self.current_player.stop()
            self.is_playing = False

def is_edit_audio(title):
    edit_keywords = ['edit', 'edits', 'slowed', 'reverb', 'sped up', 'nightcore', 'remix', '8d', '8d audio']
    return any(keyword in title for keyword in edit_keywords)

async def search_youtube(query):
    query = query.lower().replace('play', '').strip()
    search_query = f"{query} song"
    videos_search = VideosSearch(search_query, limit=10)
    results = videos_search.result()
    if results['result']:
        for result in results['result']:
            title = result['title'].lower()
            if all(word in title for word in query.split()) and not is_edit_audio(title):
                return result['link']

    print(f"Couldn't find an exact match for '{query}'. Here's the closest non-edit result:")
    for result in results['result']:
        if not is_edit_audio(result['title'].lower()):
            return result['link']
    return None

async def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s'
    }
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))

def get_audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000

def play_audio():
    global is_music_playing
    music_player = instance.media_player_new()
    media = instance.media_new('audio.mp3')
    music_player.set_media(media)
    music_player.play()
    audio_length = get_audio_length('audio.mp3')
    with open('bot_status.txt', 'w') as f:
        f.write('busy')
    print(f"Playing audio with length: {audio_length} seconds")
    with sr.Microphone() as source:
        speak_text("Playing your requested song", source)
        is_music_playing = True
        listen_for_stop(source, music_player)
        if stop_tts_flag:
            music_player.stop()
            with open('bot_status.txt', 'w') as f:
                f.write('ready')
        if os.path.exists("audio.mp3"):
            try:
                os.remove("audio.mp3")
            except PermissionError:
                print("Failed to delete output.mp3: File is still in use. Retrying...")
                time.sleep(1) 
                if os.path.exists("output.mp3"):
                    os.remove("output.mp3")
                    with open('bot_status.txt', 'w') as f:
                        f.write('ready')
    return audio_length

def listen_for_stop(source, player):
    global stop_tts_flag
    r = sr.Recognizer()
    while player.is_playing():
        try:
            audio = r.listen(source)
            prompt = r.recognize_google(audio)
            print(f"Heard during playback: {prompt}")
            if "stop" in prompt.lower():
                stop_tts_flag = True
                break
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Error in stop listener: {e}")

def speak_text(text, source):
    global is_tts_speaking, stop_tts_flag
    is_tts_speaking = True
    stop_tts_flag = False
    busy_from_start = False
    with open('bot_status.txt', 'r') as f:
            status = f.read().strip()
    if status == "busy":
        busy_from_start = True
    else:
        with open('bot_status.txt', 'w') as f:
            f.write('busy')
    try:
        tts = gTTS(text, lang='en')
        tts.save("output.mp3")
        player = instance.media_player_new()
        media = instance.media_new("output.mp3")
        player.set_media(media)
        player.play()
        time.sleep(0.5)
        while player.is_playing():
            r = sr.Recognizer()
            try:
                audio = r.listen(source)
                prompt = r.recognize_google(audio)
                print(f"Heard during TTS: {prompt}")
                if "stop" in prompt.lower():
                    stop_tts_flag = True
                    break
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
            if stop_tts_flag:
                player.stop()
                with open('bot_status.txt', 'w') as f:
                    f.write('ready')
                break
            time.sleep(0.1)
        player.stop()

    except Exception as e:
        print(f"Error in TTS: {e}")
    finally:
        if player:
            player.stop()
        if os.path.exists("output.mp3"):
            try:
                os.remove("output.mp3")
            except PermissionError:
                time.sleep(1)
                if os.path.exists("output.mp3"):
                    os.remove("output.mp3")
        is_tts_speaking = False
        if not busy_from_start:
            with open('bot_status.txt', 'w') as f:
                f.write('ready')

def stop_tts():
    global stop_tts_flag
    stop_tts_flag = True

def analyze_movement_keywords(prompt):
    patterns = [
        r'what (?:am|are|is) (?:i|you|he|she|they|it|we|the|this|that|these|those) doing',
        r'what(?:\'s|\s+is) happening',
    ]
    prompt_lower = prompt.lower()
    return any(re.search(pattern, prompt_lower) for pattern in patterns)

def is_music_command(prompt):
    return prompt.lower().startswith('play ')

def park_timer(seconds):
    time.sleep(seconds)

async def is_parked(place):
    if place == "chargingstation" or "living_room_parked" or "bedroom2_parked":
        return True
    else:
        return False

async def continuous_listen_and_respond():
    global is_music_playing, is_tts_speaking, stop_tts_flag
    r = sr.Recognizer()
    groq_client = Groq()
    together_client = Together()
    music_player = MusicPlayer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        speak_text("Adjusting for ambient noise. Please wait.", source)
        r.adjust_for_ambient_noise(source, duration=2)
        print("Ready! Speak your question...")
        speak_text("Ready! Speak your question or say 'play' followed by a song name.", source)
        park_timer = None
        while True:
            try:
                with open('bot_status.txt', 'r') as f:
                    text = f.read().strip().split()
                    status = text[0]
                    place = text[1]
                if is_music_playing or is_tts_speaking or status == "moving":
                    time.sleep(1)
                    if not park_timer.done():
                        park_timer.cancel()
                    continue
                if not is_parked(place) and park_timer.done():
                    await park_timer
                    bot.park(place)
                audio = r.listen(source)
                prompt = r.recognize_google(audio)
                print(f"\nYou said: {prompt}")
                if "alexa" not in prompt.split():
                    continue
                playsound3("listening.mp3")
                prompt = text.split("alexa", 1)[-1].strip()
                if not prompt:
                    while not prompt:
                        prompt = r.recognize_google(audio)
                if "stop" in prompt.lower():
                    continue
                if is_weather_query(prompt):
                    park_timer.cancel()
                    weather_data = await getweather()
                    response = f"Its {weather_data['description']} with a temperature of {weather_data['temperature']}°C and feels like {weather_data['feels_like']}°C. "
                    print(f"Weather Response: {response}")
                    speak_text(response, source)
                    print("\nReady for next question...")
                    continue
                datetime_query = is_datetime_query(prompt)
                if datetime_query:
                    park_timer.cancel()
                    response = get_datetime_info(datetime_query)
                    print(f"DateTime Response: {response}")
                    speak_text(response, source)
                    print("\nReady for next question...")
                    continue
                if "play" in prompt.lower():
                    park_timer.cancel()
                    url = await search_youtube(prompt)
                    if url:
                        await download_audio(url)
                        audio_length = play_audio()
                        print(f"Pausing processing for {audio_length} seconds...")
                        is_music_playing = False
                        print("Resuming processing...")
                    else:
                        response = "I couldn't find that song. Can you try another one?"
                        print(response)
                        speak_text(response, source)
                    print("\nReady for next question...")
                    continue
                if is_color_query(prompt) or analyze_movement_keywords(prompt):
                    park_timer.cancel()
                    speak_text("Looking around...", source)
                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    if ret:
                        _, buffer = cv2.imencode('.jpg', frame)
                        image_base64 = base64.b64encode(buffer).decode('utf-8')
                        llama_vision_prompt = f"{prompt}"
                        llama_vision_response = together_client.chat.completions.create(
                            model="meta-llama/Llama-Vision-Free",
                            messages=[
                                {
                                    "role": "system",
                                    "content": """You are a robot. Give short and concise human-friendly responses that sound natural
                                    when read aloud and make your responses just maximum 1 paragraph so the user will not be bored of
                                    listening to you. You will be sent a picture along with a user prompt, I need you to respond to the
                                    prompt as if youre the one seeing the picture with your eyes. Do not say things like the
                                    \"picture\"is or  in the \"image\", instead say stuff like I see that..."""
                                },
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": llama_vision_prompt},
                                        {"type": "image_url",
                                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}",}
                                        }
                                    ]
                                }
                            ]
                        )
                        response = llama_vision_response.choices[0].message.content
                        cap.release()
                        print(f"Visual Analysis Response: {response}")
                        speak_text(response, source)
                    else:
                        response = "I couldn't see anything. Please try again."
                        print(response)
                        speak_text(response, source)
                    print("\nReady for next question...")
                    continue
                park_timer.cancel()
                completion = groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": """You are a robot. Give short and concise human-friendly responses that sound natural
                        when read aloud and make your responses just maximum 1 paragraph so the user will not be bored of listening to you."""},
                        {"role": "user", "content": prompt},
                    ]
                )
                response = completion.choices[0].message.content
                print(f"Groq/Llama Response: {response}")
                speak_text(response, source)
                print("\nReady for next question...")
                speak_text("Ready for your next question.", source)
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                error_msg = f"Speech recognition error: {e}"
                print(error_msg)
                speak_text(error_msg, source)
            except KeyboardInterrupt:
                print("\nStopping...")
                if music_player.is_playing:
                    music_player.stop()
                break

if __name__ == "__main__":
    asyncio.run(continuous_listen_and_respond())