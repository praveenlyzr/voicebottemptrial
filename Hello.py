import os
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
from PIL import Image
import streamlit as st
from lyzr import VoiceBot

# Create a temporary directory if it doesn't exist
if not os.path.exists('tempDir'):
    os.makedirs('tempDir')

# Setup your config
st.set_page_config(
    page_title="LyzrVoice",
    layout="wide",  # "wide" or "centered"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png"
)

# Setup your OpenAI API key
os.environ['OPENAI_API_KEY'] = st.secrets["apikey"]
vb = VoiceBot(api_key = st.secrets["apikey"])

# Function definitions (text_to_notes, transcribe, save_uploadedfile, etc.) go here...
def lyzr_voice_persona(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-turbo",
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

def save_uploadedfile(uploaded_file):
    with open(os.path.join('tempDir', uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"Saved File: {uploaded_file.name} to tempDir")

    
def get_transformed_text(format_type):
    transformed_text_context = f"answer this like a {format_type}"
    full_transcript = transcript + "\n\n" + transformed_text_context
    transformed_text = lyzr_voice_persona(full_transcript)  
    return transformed_text


# # Load and display the logo
image = Image.open("lyzr-logo.png")
st.image(image, width=150)
st.title("LyzrVoice Demo")

st.caption('Note: The recording will stop as soon as you pause/stop speaking. Please continue to speak without a break to get the full transcript.')

recorded = False


with st.container():  
    recording, playback = st.columns(2)
    with recording:
        audio_bytes = audio_recorder()  
    #records audio
    if audio_bytes:
        with open('tempDir/output.wav', 'wb') as f:
            f.write(audio_bytes)
        transcript = vb.transcribe('tempDir/output.wav')
        transcript = st.text_area("Transcript", transcript, height=150)
        
        # Display buttons and handle their click actions
        st.write("Transform Transcript Into:")
        conv, btn_col1, btn_col2, btn_col3, btn_col4, btn_col5, btn_col6, btn_col7, btn_col8 = st.columns(9)
        transformed_text = "a conversation reply"
        with conv:
            st.write("Convert into:")
        with btn_col1:
            if st.button("Notes"):
                transformed_text = "notes or bullet points"
        with btn_col2:
            if st.button("Email"):
                transformed_text = "email to be sent"
        with btn_col3:
            if st.button("Todo"):
                transformed_text = "todo list"
        with btn_col4:
            if st.button("Summary"):
                transformed_text = "summary"
        with btn_col5:
            if st.button("Tweet"):
                transformed_text = "tweet"
        with btn_col6:
            if st.button("LinkedIn"):
                transformed_text = "linkedin post"
        with btn_col7:
            if st.button("SMS"):
                transformed_text = "sms"
        with btn_col8:
            if st.button("LinkedIn DM"):
                transformed_text = "LinkedIn DM"
        transcript = get_transformed_text(transformed_text)
        transcript = st.text_area("Response", value=transcript, height=150)
        recorded = True
    else:
        transcript = ""  # No transcript available initially

# # Text area for transcript display and editing
# transcript = st.text_area("Transcript", transcript, height=150)

# Generate TTS from transcript if any
if transcript and recorded:
    vb.text_to_speech(transcript)
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