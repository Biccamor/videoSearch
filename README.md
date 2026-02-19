# VideoSearch

VideoSearch is a Python application that enables semantic search within your video files. Using natural language queries, you can find specific moments in a video based on its visual content (what's happening on screen) or its spoken dialogue (what's being said).

The application provides both a user-friendly web interface built with Streamlit and a command-line interface for terminal users

## How It Works

The system processes and indexes a video file to make it searchable. This process happens once per video and involves two parallel pipelines:

1.  **Visual Processing**:
    *   The video is sampled into individual frames (e.g., one frame per second).
    *   Each frame is passed through the `SigLIP2` vision model to generate a vector embedding that represents its visual content.
    *   These embeddings are stored in a `LanceDB` vector database, mapped to their corresponding timestamps.

2.  **Audio Processing**:
    *   The audio track is extracted from the video file using `ffmpeg`.
    *   The `Faster Whisper` model transcribes the audio into text, complete with word-level timestamps.
    *   The transcript is grouped into logical segments (e.g., complete sentences or chunks of a minimum word count).
    *   Each text segment is converted into a vector embedding using the `all-MiniLM-L6-v2` sentence transformer.
    *   These audio text embeddings are stored in a separate `LanceDB` table, along with their start and end times.

When you perform a search, your text query is converted into a vector embedding. The system then performs a cosine similarity search against the appropriate database (visual or audio) to find the moments in the video that are most relevant to your query.

## Features

*   **Search by Visuals**: Find scenes by describing objects, actions, or settings (e.g., "a person driving a red car").
*   **Search by Audio**: Find moments based on spoken words or phrases.
*   **Combined Search**: Run both visual and audio searches simultaneously to compare results.
*   **Web Interface**: An interactive UI powered by Streamlit for easy video upload and search.
*   **Terminal Interface**: A script for command-line-based interaction.
*   **Efficient Indexing**: Uses LanceDB for fast, persistent vector storage and similarity search.

## Technologies Used

*   **Core Framework**: Streamlit
*   **Vector Database**: LanceDB
*   **Models**:
    *   **Vision/Text**: `google/siglip2-base-patch16-224` for visual frame and text query embedding.
    *   **Audio Transcription**: `faster-whisper` (medium model) for speech-to-text.
    *   **Audio Text Embedding**: `sentence-transformers/all-MiniLM-L6-v2` for transcript embedding.
*   **Libraries**:
    *   `transformers`
    *   `torch`
    *   `opencv-python`
    *   `pyarrow`
    *   `ffmpeg` (as a system dependency)

## Setup and Usage

### Prerequisites

*   Python 3.8+
*   FFmpeg: You must have `ffmpeg` installed and available in your system's PATH. You can download it from the [official ffmpeg website](https://ffmpeg.org/download.html).

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Biccamor/videoSearch.git
    cd videoSearch
    ```
2.  Install the required Python packages. It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt 
    # Or manually: pip install streamlit lancedb transformers torch sentence-transformers opencv-python pyarrow faster_whisper filetype
    ```

### Running the Application

#### Web UI (Recommended)

1.  Launch the Streamlit application:
    ```bash
    streamlit run main.py
    ```
2.  Open your web browser and navigate to the local URL provided by Streamlit.
3.  Upload an `.mp4` video file. The application will process and index it.
4.  Select a search mode and enter your query to find moments in the video.

#### Terminal UI

1.  Place your video file in the root of the project.
2.  Run the terminal script:
    ```bash
    python terminal_main.py
    ```
3.  Follow the on-screen prompts to choose a search mode and enter your query.

## Project Structure

```
.
├── data/                  # Directory for LanceDB database files (auto-generated)
├── temp_videos/           # Temporary storage for uploaded videos (auto-generated)
├── database.py            # Manages LanceDB connection and table schemas.
├── main.py                # Entry point for the Streamlit web application.
├── terminal_main.py       # Entry point for the command-line interface.
└── engines/
    ├── hearing_model.py   # Handles audio extraction, transcription, and embedding.
    ├── model.py           # Implements the visual search engine using SigLIP.
    └── video_conversion.py# Handles video-to-frame conversion and embedding.
