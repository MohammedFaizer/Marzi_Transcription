# # example.py
# import os
# from dotenv import load_dotenv
# from io import BytesIO
# import requests
# from elevenlabs.client import ElevenLabs
# import streamlit as st

# load_dotenv()



# st.title("Marzi Transcript & Diarization📝")


# uploaded_file = st.sidebar.file_uploader("Upload an MP3 file", type=["mp3"])

# if uploaded_file is not None:
#     with st.spinner("Transcribing..."):
#         audio_data = BytesIO(uploaded_file.read())
#         try:
#             transcription = elevenlabs.speech_to_text.convert(
#             file=audio_data,
#             model_id="scribe_v1", # Model to use, for now only "scribe_v1" is supported
#             tag_audio_events=True, # Tag audio events like laughter, applause, etc.
#             language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
#             diarize=True, # Whether to annotate who is speaking
#             )
#         except Exception as e:
#             st.error(f"Error during transcription: {e}")
    

#         st.text_area("Full Transcription", transcription.text, height=100)
#         dialogues = []
#         current_speaker = None
#         current_text = ""

#         for word in transcription.words:
#             if word.type == "spacing":
#                 current_text += word.text
#                 continue

#             if word.speaker_id != current_speaker:
#                 if current_text.strip():
#                     speaker_label = "User1" if current_speaker == "speaker_0" else "User2"
#                     dialogues.append({"role":"user", "content":f"**{speaker_label}:** {current_text.strip()}" })
#                 current_speaker = word.speaker_id
#                 current_text = word.text
#             else:
#                 current_text += word.text

#         # Append last speaker's text
#         if current_text.strip():
#             speaker_label = "User1" if current_speaker == "speaker_0" else "User2"
#             dialogues.append({"role":"user2", "content":f"**{speaker_label}:** {current_text.strip()}" })
           

#         # In Streamlit or console
#         for line in dialogues:
#             if line["role"] == "user":
#                 st.success(line["content"])
#             elif line["role"] == "user2":
#                 st.info(line["content"])



import streamlit as st
import requests

st.title("Marzi Transcript & Diarization📝")

file = st.sidebar.file_uploader("Upload an MP3 file", type=["mp3"])

if file is not None:
    try:
        files = {"file": (file.name, file, "audio/mpeg")}
        response = requests.post(
            "https://staging-marzi-backend.cyces.co/api/chat/transcript/",
            files=files,
        )
        data=response.json()["data"]
    
        st.text_area("Full Transcription", data["text"], height=200)
        for msg in data["dialogues"]:
            roles=""
            
            if msg["role"] == "User1":
                roles="human"
            
            elif msg["role"] == "User2":
                roles="ai"
                
            with st.chat_message(roles):
                st.write(msg["content"])
    except Exception as e:
        st.error(f"Oopsie ! Error occured during transcription")

