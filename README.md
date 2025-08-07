# CallSense

CallSense is a web application for analyzing customer support call recordings. It provides audio transcription and basic audio quality analysis via a simple web interface.

![Customer Support Icon](customer_support_icon.JPG)

---

## Features

- User login system (demo credentials: `user` / `pass`)
- Upload and analyze call recordings (supports WAV, MP3, M4A, etc.)
- Automatic transcription using Google Speech Recognition
- Displays audio properties (frame rate, channels)
- Clean, modern HTML frontend (Bootstrap)
- Example data and sample audio included

---

## Project Structure

```
CallSense/
│
├── app.py                      # Flask backend
├── model_from_notebook.py      # Audio analysis logic
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates (login, upload, result)
│     ├── login.html
│     ├── upload.html
│     └── result.html
├── sample_customer_call.wav    # Example audio file
├── customer_call_transcriptions.csv # Example CSV for advanced analysis
├── customer_support_icon.JPG   # Project icon
└── README.md                   # Project documentation
```

---

## Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/vaibhav997919/CallSense.git
cd CallSense
```

### 2. Install Python dependencies

```sh
pip install -r requirements.txt
```

### 3. Install ffmpeg

- Download from [ffmpeg.org](https://ffmpeg.org/download.html) or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
- Extract and add the `bin` folder to your system PATH.
- Verify with `ffmpeg -version` in a new terminal.

### 4. Run the app

```sh
python app.py
```

### 5. Open your browser and go to

```
http://127.0.0.1:5000/
```

### 6. Login credentials (default)

- Username: `user`
- Password: `pass`

---

## Usage

1. **Login** with the demo credentials.
2. **Upload** a call recording (WAV, MP3, M4A, etc.).
3. **View** the transcription and audio properties.
4. **Analyze another file** or logout.

---

## Notes

- You can upload audio files in WAV, MP3, M4A, and other common formats.
- The app will transcribe the audio and show basic audio properties.
- For more features or customizations, see the code and comments.

---

## License

This project is for educational/demo purposes. For production use, please review and update authentication and security.

---

## Author

[vaibhav997919](https://github.com/vaibhav997919)