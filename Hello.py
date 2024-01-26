import os
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
from PIL import Image
import streamlit as st

# Create a temporary directory if it doesn't exist
if not os.path.exists('tempDir'):
    os.makedirs('tempDir')

# Setup your config
st.set_page_config(
    page_title="LyzrVoice",
    layout="centered",  # or "wide" 
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png"
)

# Setup your OpenAI API key
os.environ['OPENAI_API_KEY'] = st.secrets["apikey"]

# Function definitions (text_to_notes, transcribe, save_uploadedfile, etc.) go here...
def text_to_notes(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are Lyzr.\n\n*Lyzr takes a momentary, stylish pause before engaging...*\n\n**User**: Can you explain how the transcription feature works?\n\n**Lyzr**: Absolutely, my friend! Here's the deal: Imagine having a superpower that lets you understand and transcribe languages and accents from all over the world with incredible accuracy. That's what I do with the transcription feature. When you speak to me or upload an audio file, I put my arsenal of advanced neural networks to work. They're like my brain's super-boosted processors, finely tuned to catch every nuance in speech. Just as a maestro can perfectly transcribe a symphony by ear, I transform spoken words into written text, making sure no detail is lost. This feature is perfect for capturing every word of your meetings, interviews, or any moment you need to convert speech into a clear, readable format. Pretty cool, right?\n\n*Remember, Lyzr takes a brief, fashionable pause before answering to give each question the thought and consideration it deserves.*"
            },
            {
                "role": "user",
                "content": f"{text}"
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    notes = response.choices[0].message.content
    return notes

def transcribe(location):
    client = OpenAI()
    
    with open(location, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            prompt="lyzr" 
        )
    return transcript.text

def save_uploadedfile(uploaded_file):
    with open(os.path.join('tempDir', uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"Saved File: {uploaded_file.name} to tempDir")

def text_to_speech(text, model="tts-1-hd", voice="echo"):
    api_key = st.secrets["apikey"] # Replace with your Streamlit secrets path
    
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text, 
    )
    
    # Save the synthesized speech to a file named "tts_output.mp3"
    response.stream_to_file("tts_output.mp3")
    

    #with col1:
        #audio_bytes = audio_recorder()
    


# # Load and display the logo
image = Image.open("lyzr-logo.png")
# col3, col4 = st.columns(2)
# # App title and introduction
st.image(image, width=150)
st.title("LyzrVoice Demo")
# with col3:
    
    
# with col4:
    
    
# st.markdown("### Welcome to LyzrVoice!")
# st.markdown("Upload an audio recording or record your voice directly, and let the AI assist you with your questions.")


# # Start of the main container

# st.markdown("#### 🎤 Record or Upload")
st.caption('Note: The recording will stop as soon as you pause/stop speaking. Please continue to speak without a break to get the full transcript.')

recorded = False

with st.container():
    recording, playback = st.columns(2)
    with recording:
        audio_bytes = audio_recorder()   
    
    if audio_bytes:
        # Record audio
        # st.audio(audio_bytes, format="audio/wav")
        with open('tempDir/output.wav', 'wb') as f:
            f.write(audio_bytes)
        transcript = transcribe('tempDir/output.wav')
        transcript = st.text_area("Transcript", transcript, height=150)
        transcript = text_to_notes(transcript)
        transcript = st.text_area("Response", transcript, height=150)
        recorded = True
    else:
        transcript = ""  # No transcript available initially

# # Text area for transcript display and editing
# transcript = st.text_area("Transcript", transcript, height=150)

# Generate TTS from transcript if any
if transcript and recorded:
    text_to_speech(transcript)
    # Display the speaker icon and TTS audio if generated
    tts_audio_file = 'tts_output.mp3'
    if os.path.isfile(tts_audio_file):
        with playback:
            st.audio(tts_audio_file, format='audio/mp3', start_time=0)      
            
            
st.markdown("---")
# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Core to generate response from transcribed audio. The audio transcription is powered by OpenAI's Whisper model. For any inquiries or issues, please contact Lyzr.
    
    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
    st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)