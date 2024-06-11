# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from openai import OpenAI
client = OpenAI()
import inspect
import textwrap
from pathlib import Path
import streamlit as st


def transcribe(location):
    client = OpenAI()
    audio_file= open(location, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text

def text_to_speech(text):
    speech_file_path = "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path



