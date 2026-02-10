"""
Audio Utilities for Viral Reel Generation
Handles TTS and Background Music Mixing
"""

from gtts import gTTS
from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips
import os

def generate_tts(text, output_path):
    """
    Generate TTS audio from text using gTTS
    """
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        return output_path
    except Exception as e:
        print(f"❌ TTS Generation Error: {e}")
        return None

def mix_audio(voice_clip_path, background_music_path, output_path, bg_volume=0.2):
    """
    Mix voiceover with background music
    """
    try:
        voice_clip = AudioFileClip(voice_clip_path)
        
        if background_music_path and os.path.exists(background_music_path):
            bg_clip = AudioFileClip(background_music_path).volumex(bg_volume)
            # Loop bg music if it's shorter than voiceover
            if bg_clip.duration < voice_clip.duration:
                bg_clip = bg_clip.loop(duration=voice_clip.duration)
            else:
                bg_clip = bg_clip.subclip(0, voice_clip.duration)
            
            final_audio = CompositeAudioClip([bg_clip, voice_clip])
        else:
            final_audio = voice_clip
            
        final_audio.write_audiofile(output_path, fps=44100)
        return output_path
    except Exception as e:
        print(f"❌ Audio Mixing Error: {e}")
        return None
