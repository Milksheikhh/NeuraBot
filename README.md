# 🤖 Intelligent Robot Control System

[![Work in Progress](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow.svg)](https://github.com/milksheikhh/NeuraBot)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)

An intelligent robot control system that combines voice recognition, AI-powered responses, music playback, weather information, and web-based room navigation. The system features both voice command processing and a web interface for controlling robot movement between different rooms.

## ✨ Features

### 🎤 Voice Control
- **Speech Recognition**: Real-time voice command processing using Google Speech Recognition
- **AI-Powered Responses**: Integration with Groq and Together AI for intelligent conversation
- **Text-to-Speech**: Natural voice responses using Google Text-to-Speech (gTTS)
- **Continuous Listening**: Always-on voice command detection

### 🎵 Music & Entertainment
- **YouTube Music Search**: Automatic song search and playback from YouTube
- **Audio Processing**: High-quality audio extraction and playback using VLC
- **Voice-Controlled Playback**: Start, stop, and control music with voice commands
- **Smart Filtering**: Automatically filters out low-quality audio edits

### 🌤️ Weather Integration
- **Real-time Weather**: Current weather conditions for Euless, TX
- **Detailed Information**: Temperature, humidity, wind speed, and "feels like" temperature
- **Voice Queries**: Ask for weather updates using natural language

### 🏠 Room Navigation
- **Web Interface**: Modern, responsive web dashboard for robot control
- **Multi-Room Support**: Navigate between bedroom1, bedroom2, living room, and charging station
- **Status Monitoring**: Real-time robot status and location tracking
- **Smart Movement**: Intelligent pathfinding between rooms

### 🔍 Computer Vision
- **Camera Integration**: OpenCV-based image processing
- **Color Recognition**: Identify colors of objects in the robot's field of view
- **Visual Analysis**: Process and analyze visual input for intelligent responses

### 📅 Utility Functions
- **Date & Time**: Voice-activated current date and time queries
- **Smart Parsing**: Natural language processing for various query types

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio processing)
- Webcam/Camera (for computer vision features)
- Microphone (for voice commands)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/robot.git
   cd robot
   ```

2. **Install required packages**
   ```bash
   pip install flask opencv-python speechrecognition groq together yt-dlp python-vlc python-weather gtts pydub playsound3 youtubesearchpython
   ```

3. **Set up FFmpeg**
   - Download and install FFmpeg
   - Update the `FFMPEG_DIR` path in `main.py` to match your installation

4. **Configure API Keys**
   - Get API keys for Groq and Together AI
   - Update the environment variables in `main.py`:
     ```python
     os.environ["GROQ_API_KEY"] = "your_groq_api_key"
     os.environ["TOGETHER_API_KEY"] = "your_together_api_key"
     ```

### Running the Application

1. **Start the voice control system**
   ```bash
   cd botfunctions
   python main.py
   ```

2. **Launch the web interface** (in a separate terminal)
   ```bash
   cd botfunctions
   python app.py
   ```

3. **Access the web dashboard**
   - Open your browser and go to `http://localhost:2000`
   - Use the interface to control robot movement between rooms

## 🎮 Usage

### Voice Commands
- **Music**: "Play [song name]" or "Stop"
- **Weather**: "What's the weather?" or "How's the temperature?"
- **Time**: "What time is it?" or "What's the date?"
- **Colors**: "What color is this?" (while pointing camera at object)
- **Movement**: Various movement commands (see code for specifics)

### Web Interface
- Click room buttons to send the robot to different locations
- Monitor real-time status through the status banner
- Visual feedback for command confirmation and robot status

## 📁 Project Structure

```
robot/
├── botfunctions/
│   ├── app.py              # Flask web application
│   ├── main.py             # Main voice control system
│   ├── bot_movement.py     # Robot movement logic
│   ├── bot_status.txt      # Robot status tracking
│   ├── listening.mp3       # Audio feedback file
│   └── templates/
│       └── index.html      # Web interface template
└── README.md
```

## 🔧 Configuration

### Room Layout
The system supports navigation between:
- **bedroom1**: Primary bedroom
- **bedroom2**: Secondary bedroom  
- **living_room**: Main living area
- **charging_station**: Robot charging dock

### Status System
- **ready**: Robot is available for commands
- **busy**: Robot is currently executing a task
- **moving**: Robot is in transit between rooms

## 🚧 Work in Progress

This project is actively under development. Current areas of focus:

- [ ] Enhanced movement algorithms
- [ ] Additional voice command recognition
- [ ] Improved error handling and recovery
- [ ] Mobile app integration
- [ ] Advanced computer vision features
- [ ] Multi-language support
- [ ] Cloud integration for remote control

## 🤝 Contributing

This project is currently in development. Contributions, suggestions, and feedback are welcome!

## 📄 License

This project is currently under development. License information will be added in future releases.

## 🔗 Dependencies

- **Flask**: Web framework for the control interface
- **OpenCV**: Computer vision and image processing
- **SpeechRecognition**: Voice command processing
- **Groq**: AI-powered conversation
- **Together AI**: Advanced language model integration
- **yt-dlp**: YouTube audio extraction
- **python-vlc**: Audio playback
- **python-weather**: Weather information
- **gTTS**: Text-to-speech conversion
- **pydub**: Audio processing utilities

## 📞 Support

For questions, issues, or suggestions, please open an issue on the GitHub repository.

---

**Note**: This is a work-in-progress project. Features and documentation are continuously being updated and improved. 