# Voice Pipeline

Atlas supports button-based push-to-talk by default with optional wake-word detection.

## Components

1. **Streamlit UI** – `apps/ui_streamlit/utils/audio_io.py` captures microphone audio
   via `sounddevice` when the button is pressed.
2. **API** – `/voice/transcribe` decodes base64 audio and calls `STTService`.
3. **STTService** – uses Vosk if installed; otherwise returns a fallback message.
4. **TTSService** – uses `pyttsx3` to speak replies in a “professional butler” tone.
5. **WakeWordService** – wraps `openWakeWord` for future wake-word support.

## Installing Vosk

```powershell
pip install vosk==0.3.45
# Download model
Invoke-WebRequest -Uri https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -OutFile model.zip
Expand-Archive model.zip -DestinationPath %USERPROFILE%\vosk
setx VOSK_MODEL_PATH %USERPROFILE%\vosk\vosk-model-small-en-us-0.15
```

Edit `.env` `VOICE_LANG` to `en` (default) or other model codes.

## Push-to-talk tips

* Microphone drop-down lists `sounddevice.query_devices()`. Use `Settings > System > Sound`
  to rename input devices for clarity.
* If audio recording fails, ensure Python has microphone permission (Windows > Privacy).

## Wake-word mode

1. Install `openwakeword` via `pip install openwakeword` (already listed in requirements).
2. Toggle the wake-word option in the Voice & Control page once microphone capture works.
3. For Porcupine substitution, comment instructions exist in `audio_io.py`.

## Troubleshooting

* Static or silence? Reduce input gain or switch to a USB headset.
* Speech not recognised? Ensure the sample rate is 16 kHz and the selected model matches
  your language (update `VOICE_LANG`).
* TTS silent? `pyttsx3` uses the default Windows voice; verify *Narrator* is enabled.
