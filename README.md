# AI Assistant PoC for Tech-Interrupt 2024

This project is a proof of concept for an AI Assistant that uses Kafka for streaming data, Deepgram for speech-to-text (STT), and Cohere for natural language processing (NLP).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- Kafka server running locally or accessible remotely
- Deepgram API key
- Cohere API key

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/WebdeveloperIsaac/genai-powered-online-voice-assistant.git
    cd ai_assistant_poc
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Set up your API keys in the `ai_assistant_poc.py` file:

    ```python
    DEEPGRAM_API_KEY = "your_deepgram_api_key"
    COHERE_API_KEY = "your_cohere_api_key"
    ```

2. Ensure your Kafka server is running and accessible. Update the Kafka consumer configuration if necessary:

    ```python
    consumer = KafkaConsumer(
        'streamingsource',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    ```

## Usage

1. Run the script:

    ```sh
    python ai_assistant_poc.py
    ```

2. The script will connect to the Kafka topic `streamingsource`, fetch messages, and process them using Deepgram and Cohere APIs.

## File Structure

- `ai_assistant_poc.py`: Main script for the AI Assistant PoC.
- `requirements.txt`: List of required Python packages.

## Dependencies

- `pyaudio`: For audio input/output.
- `wave`: For handling WAV files.
- `requests`: For making HTTP requests to APIs.
- `kafka-python`: For Kafka consumer.
- `audioOutputTest`: Custom module for audio output testing.

## Troubleshooting

- Ensure your Kafka server is running and accessible.
- Verify that your API keys are correct and have the necessary permissions.
- Check the console output for any error messages and resolve them accordingly.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Deepgram](https://deepgram.com) for the speech-to-text API.
- [Cohere](https://cohere.ai) for the natural language processing API.
- [Kafka](https://kafka.apache.org) for the streaming platform.
