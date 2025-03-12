# 🥁 Real-Time Virtual Air Drumset with Hand Tracking

![Drumset Demo](demo/demo.gif) <!-- Add actual demo gif path -->

An interactive virtual drumset that lets you play drums in mid-air using hand tracking technology. Combines computer vision with real-time audio feedback to create an immersive musical experience.

## 🎯 Key Features

- **Real-Time Hand Tracking**: MediaPipe's BlazePalm model with 21 landmark points per hand
- **Virtual Drum Interface**: 5 customizable drum pads (kick, snare, hihat, crash, tom)
- **Low-Latency Audio**: Pygame mixer with optimized WAV file playback (<50ms latency)
- **Visual Feedback System**: 
  - Real-time hand landmark visualization
  - Drum pad activation highlights
  - On-screen drum labels
- **Anti-Spam Mechanism**: Intelligent cooldown system (0.5s default)
- **Mirror Mode**: Horizontal flip for natural playing experience
- **Cross-Platform**: Compatible with Windows, macOS, and Linux

## 📁 Project Files and Functionality

### `handtrackingmodule.py` (Core Tracking Engine)
**Purpose**: Hand detection and landmark processing module  
**Functionality**:
- Initializes MediaPipe Hands model
- Processes RGB frames for hand detection
- Draws hand landmarks and connections
- Extracts normalized landmark coordinates
- Provides finger position data to main application

**Key Methods**:
- `find_hands()`: Detects hands in frame and draws landmarks
- `find_position()`: Returns list of landmark coordinates

### `virtual_drum.py` (Main Application)
**Purpose**: Manages drumset interface and user interaction  
**Functionality**:
- Initializes Pygame audio system
- Loads and manages drum sound assets
- Defines drum pad regions and visual elements
- Implements collision detection system
- Manages audio cooldown timers
- Displays real-time feedback overlay

**Core Components**:
- **Drum Regions**: Customizable positions/sizes (x, y, w, h)
- **Sound Manager**: WAV file loader with channel pooling
- **Collision Engine**: Index finger tip position validation
- **UI Renderer**: Dynamic pad highlighting and labels

## 🛠️ Underlying Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| Python | Core programming language | 3.8+ |
| OpenCV | Video capture & processing | 4.5+ |
| MediaPipe | Hand landmark detection | 0.10.3+ |
| Pygame | Audio playback & mixing | 2.5.2+ |
| NumPy | Coordinate calculations | 1.24+ |

## 🔄 Workflow

```mermaid
sequenceDiagram
    participant Webcam
    participant OpenCV
    participant MediaPipe
    participant DrumLogic
    participant Pygame
    
    Webcam->>OpenCV: Capture frame
    OpenCV->>MediaPipe: Send RGB frame
    MediaPipe-->>OpenCV: Return landmarks
    OpenCV->>DrumLogic: Finger positions
    DrumLogic->>Pygame: Trigger sounds
    Pygame-->>User: Audio output
    OpenCV-->>User: Visual feedback
